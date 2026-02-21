"""
Middleware for rate limiting, RBAC, request processing, and JWT validation.
"""
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from functools import wraps
from typing import Callable, List, Optional

from fastapi import HTTPException, Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.logging import get_logger
from src.config.settings import get_settings
from src.core.auth.models import Role, UserRole
from src.core.auth.jwks import JWKSManager
from src.shared.exceptions import AuthorizationError

logger = get_logger(__name__)

# Simple in-memory rate limiter (for development)
# TODO: Replace with Redis-based rate limiter in production
rate_limit_store = defaultdict(list)


class RateLimiter:
    """
    Simple rate limiter middleware.

    In production, this should be replaced with Redis-based rate limiting.
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
        Check rate limit for request.

        Args:
            request: FastAPI request

        Raises:
            HTTPException: If rate limit exceeded
        """
        # Get client identifier (IP + user agent)
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "unknown")
        client_id = f"{client_ip}:{user_agent}"

        now = datetime.now()
        window_start = now - timedelta(seconds=self.window)

        # Clean old requests
        rate_limit_store[client_id] = [
            req_time
            for req_time in rate_limit_store[client_id]
            if req_time > window_start
        ]

        # Check limit
        if len(rate_limit_store[client_id]) >= self.requests:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. Maximum {self.requests} requests per {self.window} seconds.",
            )

        # Add current request
        rate_limit_store[client_id].append(now)


# Rate limiters for different endpoints
auth_rate_limit = RateLimiter(requests=10, window=60)  # 10 req/min for auth
standard_rate_limit = RateLimiter(requests=60, window=60)  # 60 req/min for authenticated


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
        self.jwks_manager = JWKSManager(
            jwks_url=settings.better_auth_jwks_url,
            cache_ttl_minutes=5,
        )

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
            try:
                # Validate JWT using JWKS
                import jwt

                # Get unverified header to extract kid (key ID)
                unverified_header = jwt.get_unverified_header(token)
                kid = unverified_header.get("kid")

                # Fetch JWKS
                jwks = await self.jwks_manager.fetch_jwks()

                # Find the key
                key_data = None
                if kid:
                    for key in jwks.get("keys", []):
                        if key.get("kid") == kid:
                            key_data = key
                            break

                if key_data:
                    # Verify JWT signature
                    settings = get_settings()

                    # Extract algorithm from JWT header to support EdDSA and RS256
                    from jwt import PyJWK

                    unverified_header = jwt.get_unverified_header(token)
                    algorithm = unverified_header.get("alg", "RS256")

                    # Convert JWKS key data to PyJWK object
                    jwk = PyJWK.from_dict(key_data)

                    payload = jwt.decode(
                        token,
                        jwk.key,
                        algorithms=[algorithm],
                        options={
                            "verify_exp": True,
                            "verify_aud": settings.better_auth_audience is not None,
                            "verify_iss": settings.better_auth_issuer is not None,
                        },
                        audience=settings.better_auth_audience or None,
                        issuer=settings.better_auth_issuer or None,
                    )

                    # Extract user claims
                    user_id = payload.get("sub") or payload.get("user_id")
                    email = payload.get("email")

                    if user_id and email:
                        # Valid session - inject into request.state
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
                        # Missing required claims
                        request.state.user = None
                        request.state.user_id = None
                        logger.warning("JWT missing required claims (sub, email)")
                else:
                    # Key not found in JWKS
                    request.state.user = None
                    request.state.user_id = None
                    logger.warning(f"Key ID '{kid}' not found in JWKS")

            except jwt.ExpiredSignatureError:
                request.state.user = None
                request.state.user_id = None
                logger.debug("JWT token expired")

            except jwt.InvalidTokenError as e:
                # Not a JWT - might be a session token, try validating with auth server
                request.state.user = None
                request.state.user_id = None
                logger.debug(f"Not a valid JWT ({e}), trying session token validation")

                # Try session token validation
                try:
                    import httpx
                    settings = get_settings()
                    auth_server_url = settings.better_auth_jwks_url.replace('/.well-known/jwks.json', '')

                    async with httpx.AsyncClient() as client:
                        response = await client.get(
                            f"{auth_server_url}/api/auth/get-session",
                            cookies={self.cookie_name: token},
                            timeout=5.0
                        )

                        if response.status_code == 200:
                            data = response.json()
                            if data and data.get('user'):
                                user = data['user']
                                request.state.user = {
                                    "id": user.get('id'),
                                    "email": user.get('email'),
                                    "name": user.get('name'),
                                    "email_verified": user.get('emailVerified', False),
                                    "role": user.get('role', 'student'),
                                }
                                request.state.user_id = user.get('id')
                                logger.debug(f"✅ Session token validated for user {user.get('email')}")
                except Exception as session_error:
                    logger.debug(f"Session token validation also failed: {session_error}")

            except Exception as e:
                request.state.user = None
                request.state.user_id = None
                logger.warning(f"Unexpected error during JWT validation: {e}")
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

        # Log request completion
        logger.info(
            "Request completed",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_ms=round(duration_ms, 2),
            client=client_host,
            user_id=getattr(request.state, "user_id", None),
        )

        return response


def get_auth_middleware(app) -> type:
    """
    Factory function to get the authentication middleware.

    This provides compatibility with the expected BetterAuth interface.
    """
    return JWKSAuthMiddleware
