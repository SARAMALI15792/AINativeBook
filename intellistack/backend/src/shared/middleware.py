"""
Middleware for rate limiting, RBAC, request processing, and JWT validation.
"""
import redis.asyncio as redis
import uuid
from datetime import datetime, timedelta, timezone
from functools import wraps
from typing import Callable, List, Optional

from fastapi import HTTPException, Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.logging import get_logger
from src.config.settings import get_settings
from src.core.auth.models import Role, UserRole
from src.core.auth.jwks import JWKSManager, get_shared_jwks_manager
from src.core.auth.jwt_utils import decode_bearer_jwt
from src.shared.exceptions import AuthorizationError
from src.shared.metrics import (
    metrics,
    METRIC_HTTP_REQUESTS_TOTAL,
    METRIC_HTTP_ERRORS_TOTAL,
    METRIC_HTTP_LATENCY_MS,
    METRIC_AUTH_FAILURES_TOTAL,
    METRIC_RATE_LIMIT_HITS,
)

logger = get_logger(__name__)

# Redis rate limiter instance (initialized once)
_redis_client = None


async def get_redis_client():
    """Get or create Redis client instance."""
    global _redis_client
    if _redis_client is None:
        settings = get_settings()
        _redis_client = redis.from_url(settings.redis_url)
    return _redis_client


class RateLimiter:
    """
    Redis-based rate limiter middleware.

    Uses Redis for distributed rate limiting across multiple server instances.
    """

    def __init__(self, requests: int, window: int):
        """
        Initialize rate limiter.

        Args:
            requests: Number of requests allowed
            window: Time window in seconds
        """
        self.requests = requests
        self.window = window

    async def __call__(self, request: Request):
        """
        Check rate limit for request using Redis.

        Args:
            request: FastAPI request

        Raises:
            HTTPException: If rate limit exceeded
        """
        # Get client identifier (IP + user agent)
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "unknown")
        client_id = f"{client_ip}:{user_agent}"

        # Get Redis client
        redis_client = await get_redis_client()

        # Use Redis to implement sliding window counter
        now = datetime.now()
        window_start = now - timedelta(seconds=self.window)
        window_start_timestamp = window_start.timestamp()

        # Redis key for this client's rate limit
        key = f"rate_limit:{client_id}"

        # Start transaction
        pipe = redis_client.pipeline()

        # Remove expired entries (older than window)
        pipe.zremrangebyscore(key, 0, window_start_timestamp)

        # Count current requests
        pipe.zcard(key)

        # Add current request timestamp
        pipe.zadd(key, {str(now.timestamp()): now.timestamp()})

        # Set expiration for the key to clean up automatically
        pipe.expire(key, self.window)

        # Execute transaction
        results = await pipe.execute()
        current_requests = results[1]

        # Check if limit exceeded
        if current_requests >= self.requests:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. Maximum {self.requests} requests per {self.window} seconds.",
            )


# ---------------------------------------------------------------------------
# IP-based rate limiters (unchanged — used as Depends() on route functions)
# ---------------------------------------------------------------------------
auth_rate_limit = RateLimiter(requests=10, window=60)        # 10 req/min for auth
standard_rate_limit = RateLimiter(requests=60, window=60)    # 60 req/min for standard


class UserScopedRateLimiter:
    """
    Redis sliding-window rate limiter keyed on the **authenticated user ID**.

    Falls back to the client IP when the request is unauthenticated so that
    public endpoints are still protected against anonymous abuse.

    Intended for AI endpoints (RAG chat, tutor) that are expensive to serve
    and where per-user fairness matters more than per-IP fairness.

    Usage (as a FastAPI dependency)::

        ai_rate_limit = UserScopedRateLimiter(requests=20, window=60)

        @router.post("/chat")
        async def chat(
            _: None = Depends(ai_rate_limit),
            ...
        ):
            ...
    """

    def __init__(self, requests: int, window: int, prefix: str = "user_rl") -> None:
        self.requests = requests
        self.window = window
        self.prefix = prefix

    async def __call__(self, request: Request) -> None:
        """
        Check and increment the rate-limit counter for the current actor.

        Raises
        ------
        HTTPException(429)
            When the actor has exceeded ``self.requests`` in ``self.window`` seconds.
        """
        # Prefer authenticated user ID; fall back to client IP
        user_id: str | None = getattr(request.state, "user_id", None)
        if user_id:
            actor_key = f"{self.prefix}:user:{user_id}"
        else:
            client_ip = request.client.host if request.client else "unknown"
            actor_key = f"{self.prefix}:ip:{client_ip}"

        redis_client = await get_redis_client()
        now = datetime.now()
        window_start = now - timedelta(seconds=self.window)

        pipe = redis_client.pipeline()
        pipe.zremrangebyscore(actor_key, 0, window_start.timestamp())
        pipe.zcard(actor_key)
        pipe.zadd(actor_key, {str(now.timestamp()): now.timestamp()})
        pipe.expire(actor_key, self.window)
        results = await pipe.execute()
        current_count: int = results[1]

        if current_count >= self.requests:
            metrics.inc(METRIC_RATE_LIMIT_HITS, labels={"prefix": self.prefix})
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=(
                    f"Rate limit exceeded: maximum {self.requests} requests "
                    f"per {self.window} seconds per user."
                ),
            )


# ---------------------------------------------------------------------------
# Pre-configured user-scoped limiters for AI endpoints
# ---------------------------------------------------------------------------
# These are injected as Depends() on the individual AI route handlers.
ai_chat_rate_limit = UserScopedRateLimiter(
    requests=20, window=60, prefix="ai_chat_rl"
)   # 20 AI requests / min / user
tutor_rate_limit = UserScopedRateLimiter(
    requests=15, window=60, prefix="tutor_rl"
)   # 15 tutor requests / min / user


def require_role(*required_roles: str):
    """
    Decorator to enforce role-based access control.

    Usage:
        @require_role("admin")
        async def admin_only_endpoint(...):
            ...

        @require_role("instructor", "admin")
        async def instructor_or_admin(...):
            ...

    Args:
        *required_roles: Role names that are allowed access

    Returns:
        Decorator function

    Raises:
        HTTPException: If user lacks required role
    """

    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract current_user from kwargs (injected by Depends)
            current_user = kwargs.get("current_user")
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required",
                )

            # Extract db session
            db: AsyncSession = kwargs.get("db")
            if not db:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Database session not available",
                )

            # Check user roles
            result = await db.execute(
                select(Role.name)
                .join(UserRole)
                .where(
                    UserRole.user_id == current_user.id,
                    UserRole.revoked_at.is_(None),
                )
            )
            user_roles = {row[0] for row in result.all()}

            # Check if user has any of the required roles
            if not any(role in user_roles for role in required_roles):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Requires one of these roles: {', '.join(required_roles)}",
                )

            return await func(*args, **kwargs)

        return wrapper

    return decorator


async def check_permissions(
    db: AsyncSession,
    user_id: str,
    required_roles: List[str],
) -> bool:
    """
    Check if user has any of the required roles.

    Args:
        db: Database session
        user_id: User ID to check
        required_roles: List of role names

    Returns:
        bool: True if user has at least one required role
    """
    result = await db.execute(
        select(Role.name)
        .join(UserRole)
        .where(
            UserRole.user_id == user_id,
            UserRole.revoked_at.is_(None),
        )
    )
    user_roles = {row[0] for row in result.all()}

    return any(role in user_roles for role in required_roles)


class JWKSAuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware to extract and validate Better-Auth JWT tokens from Authorization header.

    This middleware:
    1. Extracts the Bearer token from Authorization header
    2. Validates the JWT using JWKS public keys (no auth-server call needed)
    3. Injects user context into request.state for downstream use
    4. Handles expired/invalid tokens gracefully
    5. Optional: Also checks cookies for session tokens (backward compatibility)

    JWT Validation:
    - Uses RS256 public keys from JWKS endpoint
    - 5-minute cache with exponential backoff for resilience
    - Falls back to last-known-good keys if endpoint unavailable
    """

    def __init__(self, app, cookie_name: str = None):
        super().__init__(app)
        settings = get_settings()
        self.cookie_name = cookie_name or settings.better_auth_session_cookie_name
        # Use the process-wide singleton so middleware and dependency layer
        # share a single JWKS cache (avoids duplicate fetches and stale-key races).
        self.jwks_manager = get_shared_jwks_manager()

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        # Extract token from Authorization header (preferred)
        auth_header = request.headers.get("Authorization", "")
        token = None

        logger.debug(f"Auth middleware processing path: {request.url.path}")
        logger.debug(f"Cookie name to check: {self.cookie_name}")
        logger.debug(f"Available cookies: {list(request.cookies.keys())}")

        if auth_header.startswith("Bearer "):
            token = auth_header[7:]  # Remove "Bearer " prefix
            logger.debug("Found Bearer token in Authorization header")
        else:
            # Fallback: check for session cookie
            token = request.cookies.get(self.cookie_name)
            logger.debug(f"Checking cookie '{self.cookie_name}': {'found' if token else 'not found'}")

        if token:
            logger.debug(f"Token found, attempting validation (length: {len(token)})")

            # --- Step 1: early algorithm enforcement (no network, no await) -----
            # Parse the JWT header immediately so we can reject non-EdDSA tokens
            # BEFORE any JWKS fetch.  Returning a JSONResponse here (not raising)
            # gives us full control over the error body including the specific
            # INVALID_TOKEN_ALGORITHM code that clients and tests expect.
            import jwt as _jwt

            _algorithm: str | None = None
            _is_jwt = True
            try:
                _hdr = _jwt.get_unverified_header(token)
                _algorithm = _hdr.get("alg", "EdDSA")
            except _jwt.DecodeError:
                _is_jwt = False  # not a JWT — fall through to session-token path

            if _is_jwt and _algorithm != "EdDSA":
                logger.warning(
                    "Token rejected: header claims alg=%r; only EdDSA is accepted. "
                    "Possible algorithm-confusion attack.",
                    _algorithm,
                )
                metrics.inc(METRIC_AUTH_FAILURES_TOTAL, labels={"reason": "invalid_algorithm"})
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={
                        "error": {
                            "code": "INVALID_TOKEN_ALGORITHM",
                            "message": (
                                "Token uses an unsupported signing algorithm. "
                                "Only EdDSA tokens issued by the auth server are accepted."
                            ),
                        }
                    },
                    headers={"WWW-Authenticate": "Bearer"},
                )

            # --- Step 2: full JWT/session-token validation ----------------------
            try:
                settings = get_settings()

                if _is_jwt:
                    # decode_bearer_jwt validates key lookup, key algorithm, and
                    # signature — returns the payload dict on success, or None if
                    # the token has no recognisable key ID (treated as non-JWT).
                    payload = await decode_bearer_jwt(token, self.jwks_manager, settings)
                else:
                    payload = None  # not a JWT header — go straight to session path

                if payload is not None:
                    # Valid JWT — inject user context into request.state
                    user_id = payload.get("sub") or payload.get("user_id")
                    email = payload.get("email")

                    if user_id and email:
                        request.state.user = {
                            "id": user_id,
                            "email": email,
                            "name": payload.get("name"),
                            "email_verified": payload.get("email_verified", False),
                            "role": payload.get("role", "student"),
                        }
                        request.state.user_id = user_id
                        logger.debug(f"✅ JWT validated for user {email}")
                    else:
                        request.state.user = None
                        request.state.user_id = None
                        logger.warning("JWT missing required claims (sub, email)")

                else:
                    # Not a JWT (or no kid) — try session-token validation
                    request.state.user = None
                    request.state.user_id = None
                    logger.debug("Token is not a JWT; trying session-token validation")

                    try:
                        import httpx
                        auth_server_url = settings.better_auth_jwks_url.replace(
                            "/.well-known/jwks.json", ""
                        )
                        async with httpx.AsyncClient() as http_client:
                            sess_response = await http_client.get(
                                f"{auth_server_url}/api/auth/get-session",
                                cookies={self.cookie_name: token},
                                timeout=5.0,
                            )
                        if sess_response.status_code == 200:
                            data = sess_response.json()
                            if data and data.get("user"):
                                user = data["user"]
                                request.state.user = {
                                    "id": user.get("id"),
                                    "email": user.get("email"),
                                    "name": user.get("name"),
                                    "email_verified": user.get("emailVerified", False),
                                    "role": user.get("role", "student"),
                                }
                                request.state.user_id = user.get("id")
                                logger.debug(
                                    f"✅ Session token validated for user {user.get('email')}"
                                )
                    except Exception as session_error:
                        logger.debug(f"Session-token validation failed: {session_error}")

            except HTTPException:
                # decode_bearer_jwt raised an intentional 401 — re-raise so Starlette
                # delivers it to the registered exception handlers (Phase 3.2).
                raise

            except Exception as exc:
                request.state.user = None
                request.state.user_id = None
                logger.warning(f"Unexpected error during token validation: {exc}")

        else:
            # No token provided
            request.state.user = None
            request.state.user_id = None

        # Process the request
        response = await call_next(request)

        return response


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log all requests with timing information."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        import time

        start_time = time.time()
        client_host = request.client.host if request.client else "unknown"

        # Log request start
        logger.debug(
            "Request started",
            method=request.method,
            path=request.url.path,
            client=client_host,
        )

        response = await call_next(request)

        # Calculate duration
        duration_ms = (time.time() - start_time) * 1000

        # Log request completion (include correlation ID when present)
        logger.info(
            "Request completed",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_ms=round(duration_ms, 2),
            client=client_host,
            user_id=getattr(request.state, "user_id", None),
            correlation_id=getattr(request.state, "correlation_id", None),
        )

        # --- Metrics instrumentation -----------------------------------------
        status_class = f"{response.status_code // 100}xx"
        metrics.inc(
            METRIC_HTTP_REQUESTS_TOTAL,
            labels={"method": request.method, "status_class": status_class},
        )
        metrics.observe(METRIC_HTTP_LATENCY_MS, duration_ms)
        if response.status_code >= 400:
            metrics.inc(
                METRIC_HTTP_ERRORS_TOTAL,
                labels={"status_code": str(response.status_code)},
            )

        return response


class CorrelationIDMiddleware(BaseHTTPMiddleware):
    """
    Attach a correlation / request-trace ID to every request and response.

    Behaviour
    ---------
    - If the client sends an ``X-Request-ID`` header, that value is used.
    - Otherwise a new UUID4 is generated.
    - The ID is stored on ``request.state.correlation_id`` so route handlers
      and other middleware can include it in structured log entries.
    - The same ID is added to the response as ``X-Request-ID`` so clients
      can correlate frontend logs with backend traces.
    """

    HEADER = "X-Request-ID"

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        correlation_id = request.headers.get(self.HEADER) or str(uuid.uuid4())
        request.state.correlation_id = correlation_id

        response = await call_next(request)
        response.headers[self.HEADER] = correlation_id
        return response


def get_auth_middleware(app) -> type:
    """
    Factory function to get the authentication middleware.

    This provides compatibility with the expected BetterAuth interface.
    """
    return JWKSAuthMiddleware
