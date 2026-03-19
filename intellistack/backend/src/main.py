"""FastAPI application entry point for IntelliStack API."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.config.logging import get_logger, setup_logging
from src.config.settings import Settings, get_settings
from src.shared.database import close_db, ensure_tables_created, init_db, seed_initial_data_if_needed
from src.shared.exceptions import IntelliStackError

# Centralised router registry (Phase 3.5) — replaces individual include_router calls
from src.core.routes_registry import register_all_routers

# Import middleware
from src.shared.middleware import (
    CorrelationIDMiddleware,
    JWKSAuthMiddleware,
    RequestLoggingMiddleware,
)

# Observability — Phase 4.4
from src.shared.metrics import metrics, alerts, register_default_alert_rules
from fastapi.responses import PlainTextResponse

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan - startup and shutdown events."""
    settings = get_settings()

    # Startup
    logger.info("Starting IntelliStack API", environment=settings.environment)
    setup_logging(settings)
    init_db(settings)
    register_default_alert_rules()

    # Skip auto-table creation - PostgreSQL uses Alembic migrations
    await ensure_tables_created(settings)

    # Seed initial data if needed (roles, etc.)
    await seed_initial_data_if_needed(settings)

    yield

    # Shutdown
    logger.info("Shutting down IntelliStack API")
    await close_db()


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create and configure the FastAPI application."""
    if settings is None:
        settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="IntelliStack - AI-Native Learning Platform for Physical AI & Humanoid Robotics",
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
        openapi_url="/openapi.json" if settings.debug else "/api/openapi.json",
        lifespan=lifespan,
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Correlation ID middleware — must be outermost so the ID is available to all
    # subsequent middleware and to the response logging step.
    app.add_middleware(CorrelationIDMiddleware)

    # Add JWT authentication middleware (validates Better-Auth tokens from Authorization header or cookies)
    app.add_middleware(JWKSAuthMiddleware)

    # Add request logging middleware
    app.add_middleware(RequestLoggingMiddleware)

    # -----------------------------------------------------------------------
    # Exception handlers — all responses use the standard envelope:
    #   {"error": {"code": "<SNAKE_CODE>", "message": "...", ["details": ...]}}
    # -----------------------------------------------------------------------

    # Helper: map HTTP status codes to short error codes for plain HTTPExceptions
    _STATUS_CODE_MAP = {
        400: "BAD_REQUEST",
        401: "UNAUTHORIZED",
        403: "FORBIDDEN",
        404: "NOT_FOUND",
        405: "METHOD_NOT_ALLOWED",
        409: "CONFLICT",
        422: "VALIDATION_ERROR",
        429: "RATE_LIMIT_EXCEEDED",
        500: "INTERNAL_SERVER_ERROR",
        502: "BAD_GATEWAY",
        503: "SERVICE_UNAVAILABLE",
    }

    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request, exc: HTTPException
    ) -> JSONResponse:
        """
        Standardise ALL HTTPException responses to the canonical error envelope.

        Handles three detail shapes:
        * str  → wrapped in {"error": {"code": ..., "message": detail}}
        * dict already containing "error" key → passed through unchanged
        * any other dict/object → stringified and wrapped
        """
        detail = exc.detail
        if isinstance(detail, dict) and "error" in detail:
            # Already in standard shape (e.g. raised via IntelliStackError.to_dict())
            content = detail
        elif isinstance(detail, str):
            code = _STATUS_CODE_MAP.get(exc.status_code, "HTTP_ERROR")
            content = {"error": {"code": code, "message": detail}}
        else:
            code = _STATUS_CODE_MAP.get(exc.status_code, "HTTP_ERROR")
            content = {"error": {"code": code, "message": str(detail)}}

        logger.warning(
            "HTTP error",
            status_code=exc.status_code,
            path=request.url.path,
            detail=detail,
        )
        return JSONResponse(
            status_code=exc.status_code,
            headers=dict(exc.headers or {}),
            content=content,
        )

    @app.exception_handler(IntelliStackError)
    async def intellistack_exception_handler(
        request: Request, exc: IntelliStackError
    ) -> JSONResponse:
        """Handle custom IntelliStack exceptions (already in standard envelope)."""
        logger.warning(
            "Request failed",
            error_code=exc.error_code,
            message=exc.message,
            path=request.url.path,
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.to_dict(),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        """Return structured 422 for request body / query-param validation failures."""
        errors = [
            {
                "field": " → ".join(str(loc) for loc in err["loc"]),
                "message": err["msg"],
                "type": err["type"],
            }
            for err in exc.errors()
        ]
        logger.warning(
            "Request validation failed",
            path=request.url.path,
            errors=errors,
        )
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Request validation failed",
                    "details": errors,
                }
            },
        )

    @app.exception_handler(ValueError)
    async def value_error_handler(
        request: Request, exc: ValueError
    ) -> JSONResponse:
        """
        Convert unhandled ValueError into a structured 400 response.

        Route handlers should catch domain-specific ValueError themselves and
        map to the correct HTTP status. This handler is the last safety net so
        raw ValueErrors never surface as 500s.
        """
        logger.warning(
            "Unhandled ValueError",
            error=str(exc),
            path=request.url.path,
        )
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error": {
                    "code": "BAD_REQUEST",
                    "message": str(exc),
                }
            },
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        """Handle unexpected exceptions — always returns structured 500."""
        logger.error(
            "Unexpected error",
            error=str(exc),
            path=request.url.path,
            exc_info=True,
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "An unexpected error occurred. The team has been notified.",
                }
            },
        )

    # Health check endpoint
    @app.get("/health", tags=["System"])
    async def health_check() -> dict:
        """Health check endpoint."""
        from datetime import datetime
        return {
            "status": "healthy",
            "version": settings.app_version,
            "environment": settings.environment,
            "timestamp": datetime.utcnow().isoformat(),
        }

    @app.get("/health/detail", tags=["System"])
    async def health_detail() -> dict:
        """
        Detailed health check including live metric counters.

        Intended for internal / ops use — do NOT expose publicly in production
        without authentication.  Returns the same structured metrics as the
        Prometheus scrape endpoint but in JSON format.
        """
        return {
            "status": "healthy",
            "version": settings.app_version,
            "environment": settings.environment,
            "metrics": metrics.to_dict(),
        }

    @app.get("/metrics", tags=["System"], response_class=PlainTextResponse)
    async def prometheus_metrics() -> str:
        """
        Prometheus-compatible metrics endpoint (text/plain exposition format).

        Intended for scraping by Prometheus / Grafana Agent.  Protect this
        endpoint with a network policy or API gateway in production so that
        metric data is not exposed to external clients.
        """
        return metrics.to_prometheus_text()

    # API v1 router
    @app.get("/api/v1", tags=["System"])
    async def api_root() -> dict:
        """API root endpoint."""
        return {
            "name": settings.app_name,
            "version": settings.app_version,
            "docs": "/docs" if settings.debug else None,
        }

    # Register all routers via the centralised registry (see src/core/routes_registry.py)
    register_all_routers(app)

    return app


# Create app instance
app = create_app()


if __name__ == "__main__":
    import uvicorn

    settings = get_settings()
    uvicorn.run(
        "src.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )

