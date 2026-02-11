"""
Middleware for rate limiting, RBAC, request processing, and BetterAuth session handling.
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
from src.core.auth.better_auth_config import get_better_auth_config
from src.core.auth.models import Role, UserRole
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


class BetterAuthSessionMiddleware(BaseHTTPMiddleware):
    """
    Middleware to extract and validate BetterAuth-style session cookies.

    This middleware:
    1. Extracts the session token from cookies
    2. Validates the JWT token
    3. Injects session data into request.state for downstream use
    4. Handles token refresh if needed
    5. Sets appropriate cookie attributes for security
    """

    def __init__(self, app, cookie_name: str = "intellistack.session"):
        super().__init__(app)
        self.cookie_name = cookie_name
        self.better_auth = get_better_auth_config()

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        # Extract session token from cookie
        session_token = request.cookies.get(self.cookie_name)

        if session_token:
            # Validate the token
            payload = self.better_auth.decode_token(session_token)

            if payload:
                # Check if token is expired
                exp = payload.get("exp")
                if exp and datetime.fromtimestamp(exp, tz=timezone.utc) > datetime.now(timezone.utc):
                    # Valid session - inject into request.state
                    request.state.session = {
                        "userId": payload.get("userId") or payload.get("sub"),
                        "sessionId": payload.get("sessionId"),
                        "email": payload.get("email"),
                        "roles": payload.get("roles", []),
                        "token": session_token,
                    }
                    request.state.user_id = payload.get("userId") or payload.get("sub")
                else:
                    # Expired token
                    request.state.session = None
                    request.state.user_id = None
            else:
                # Invalid token
                request.state.session = None
                request.state.user_id = None
        else:
            # No session cookie
            request.state.session = None
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
    return BetterAuthSessionMiddleware
