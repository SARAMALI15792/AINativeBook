"""
Middleware for rate limiting, RBAC, and request processing.
"""
from collections import defaultdict
from datetime import datetime, timedelta
from functools import wraps
from typing import Callable, List

from fastapi import HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth.models import Role, UserRole
from src.shared.exceptions import AuthorizationError

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
