"""FastAPI application entry point for IntelliStack API."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.config.logging import get_logger, setup_logging
from src.config.settings import Settings, get_settings
from src.shared.database import close_db, ensure_tables_created, init_db, seed_initial_data_if_needed
from src.shared.exceptions import IntelliStackError

# Import routers
from src.ai.rag.routes import router as rag_router
from src.ai.chatkit.routes import router as chatkit_router
from src.core.content.routes import router as content_router
from src.core.institution.routes import router as institution_router
from src.core.learning.routes import router as learning_router
from src.core.users.routes import router as users_router
from src.core.users.preferences_routes import router as preferences_router
from src.ai.personalization.routes import router as personalization_router
from src.ai.translation.routes import router as translation_router
from src.ai.code_execution.routes import router as code_execution_router
from src.ai.tutor.routes import router as tutor_router
from src.core.content.enhanced_routes import router as enhanced_content_router

# Import middleware
from src.shared.middleware import (
    JWKSAuthMiddleware,
    RequestLoggingMiddleware,
)

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan - startup and shutdown events."""
    settings = get_settings()

    # Startup
    logger.info("Starting IntelliStack API", environment=settings.environment)
    setup_logging(settings)
    init_db(settings)

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

    # Add JWT authentication middleware (validates Better-Auth tokens from Authorization header or cookies)
    app.add_middleware(JWKSAuthMiddleware)

    # Add request logging middleware
    app.add_middleware(RequestLoggingMiddleware)

    # Exception handlers
    @app.exception_handler(IntelliStackError)
    async def intellistack_exception_handler(
        request: Request, exc: IntelliStackError
    ) -> JSONResponse:
        """Handle custom IntelliStack exceptions."""
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

    @app.exception_handler(Exception)
    async def general_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        """Handle unexpected exceptions."""
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
                    "message": "An unexpected error occurred",
                }
            },
        )

    # Health check endpoint
    @app.get("/health", tags=["System"])
    async def health_check() -> dict:
        """Health check endpoint."""
        return {
            "status": "healthy",
            "version": settings.app_version,
            "environment": settings.environment,
        }

    # API v1 router
    @app.get("/api/v1", tags=["System"])
    async def api_root() -> dict:
        """API root endpoint."""
        return {
            "name": settings.app_name,
            "version": settings.app_version,
            "docs": "/docs" if settings.debug else None,
        }

    # Register routers with API prefix
    app.include_router(content_router, prefix="/api/v1")
    app.include_router(institution_router, prefix="/api/v1")
    app.include_router(learning_router, prefix="/api/v1")
    app.include_router(rag_router, prefix="/api/v1")
    app.include_router(chatkit_router)  # ChatKit has its own /api/v1/chatkit prefix
    app.include_router(users_router)  # Users has its own /api/v1/users prefix
    app.include_router(preferences_router)  # Preferences has its own /api/v1/users/preferences prefix
    app.include_router(personalization_router)
    app.include_router(translation_router)
    app.include_router(code_execution_router)
    app.include_router(tutor_router)
    app.include_router(enhanced_content_router)

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

