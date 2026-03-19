"""
ChatKit Rate Limiter

Implements rate limiting for AI tutor messages:
- 20 messages/day for students (FR-027)
- Unlimited for instructors and admins
"""

import uuid
import logging
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import ChatKitRateLimit

logger = logging.getLogger(__name__)


# Rate limit configuration
STUDENT_DAILY_LIMIT = 20
EXEMPT_ROLES = {"instructor", "admin"}


@dataclass
class RateLimitResult:
    """Result of rate limit check."""

    allowed: bool
    remaining: int
    limit: int
    reset_at: Optional[datetime]
    message: Optional[str] = None

    @property
    def reset_timestamp(self) -> Optional[str]:
        """Get reset time as ISO string."""
        if self.reset_at:
            return self.reset_at.isoformat()
        return None

    @property
    def reset_seconds(self) -> Optional[int]:
        """Get seconds until reset."""
        if self.reset_at:
            delta = self.reset_at - datetime.utcnow()
            return max(0, int(delta.total_seconds()))
        return None


class RateLimiter:
    """
    Rate limiter for ChatKit messages.

    Enforces daily message limits for students while
    allowing unlimited access for instructors and admins.
    """

    def __init__(self, db_session: AsyncSession):
        """
        Initialize rate limiter.

        Args:
            db_session: SQLAlchemy async session
        """
        self.db = db_session

    async def check_limit(self, user_id: str, role: str) -> RateLimitResult:
        """
        Check if user is within rate limits.

        Args:
            user_id: User ID
            role: User role (student, instructor, admin)

        Returns:
            RateLimitResult indicating if request is allowed
        """
        # Exempt instructors and admins
        if role.lower() in EXEMPT_ROLES:
            return RateLimitResult(
                allowed=True,
                remaining=float("inf"),
                limit=float("inf"),
                reset_at=None,
                message=None,
            )

        # Get or create rate limit record
        stmt = select(ChatKitRateLimit).where(ChatKitRateLimit.user_id == user_id)
        result = await self.db.execute(stmt)
        rate_limit = result.scalar_one_or_none()

        now = datetime.utcnow()

        if not rate_limit:
            # Create new rate limit record
            rate_limit = ChatKitRateLimit(
                id=str(uuid.uuid4()),
                user_id=user_id,
                message_count=0,
                window_start=now,
                last_reset=now,
                is_limited=False,
            )
            self.db.add(rate_limit)
            await self.db.commit()
            await self.db.refresh(rate_limit)

        # Check if we need to reset the window (24 hours)
        window_end = rate_limit.window_start + timedelta(hours=24)
        if now >= window_end:
            # Reset window
            rate_limit.message_count = 0
            rate_limit.window_start = now
            rate_limit.last_reset = now
            rate_limit.is_limited = False
            await self.db.commit()

        # Calculate remaining and reset time
        remaining = max(0, STUDENT_DAILY_LIMIT - rate_limit.message_count)
        reset_at = rate_limit.window_start + timedelta(hours=24)

        # Check if over limit
        if rate_limit.message_count >= STUDENT_DAILY_LIMIT:
            time_until_reset = reset_at - now
            hours = int(time_until_reset.total_seconds() // 3600)
            minutes = int((time_until_reset.total_seconds() % 3600) // 60)

            return RateLimitResult(
                allowed=False,
                remaining=0,
                limit=STUDENT_DAILY_LIMIT,
                reset_at=reset_at,
                message=f"Daily message limit reached ({STUDENT_DAILY_LIMIT}/day). Resets in {hours}h {minutes}m.",
            )

        return RateLimitResult(
            allowed=True,
            remaining=remaining,
            limit=STUDENT_DAILY_LIMIT,
            reset_at=reset_at,
            message=None,
        )

    async def increment(self, user_id: str, role: str) -> RateLimitResult:
        """
        Increment message count and return updated limit status.

        Should be called after successfully processing a message.

        Args:
            user_id: User ID
            role: User role

        Returns:
            Updated RateLimitResult
        """
        # Exempt roles don't need incrementing
        if role.lower() in EXEMPT_ROLES:
            return RateLimitResult(
                allowed=True,
                remaining=float("inf"),
                limit=float("inf"),
                reset_at=None,
            )

        stmt = select(ChatKitRateLimit).where(ChatKitRateLimit.user_id == user_id)
        result = await self.db.execute(stmt)
        rate_limit = result.scalar_one_or_none()

        if not rate_limit:
            # This shouldn't happen if check_limit was called first
            return await self.check_limit(user_id, role)

        # Increment count
        rate_limit.message_count += 1
        rate_limit.is_limited = rate_limit.message_count >= STUDENT_DAILY_LIMIT

        await self.db.commit()

        # Calculate remaining
        remaining = max(0, STUDENT_DAILY_LIMIT - rate_limit.message_count)
        reset_at = rate_limit.window_start + timedelta(hours=24)

        logger.debug(
            f"User {user_id} used {rate_limit.message_count}/{STUDENT_DAILY_LIMIT} messages"
        )

        return RateLimitResult(
            allowed=True,
            remaining=remaining,
            limit=STUDENT_DAILY_LIMIT,
            reset_at=reset_at,
        )

    async def get_usage(self, user_id: str, role: str) -> dict:
        """
        Get current usage statistics for a user.

        Args:
            user_id: User ID
            role: User role

        Returns:
            Usage statistics dict
        """
        if role.lower() in EXEMPT_ROLES:
            return {
                "used": 0,
                "limit": "unlimited",
                "remaining": "unlimited",
                "reset_at": None,
                "is_limited": False,
            }

        stmt = select(ChatKitRateLimit).where(ChatKitRateLimit.user_id == user_id)
        result = await self.db.execute(stmt)
        rate_limit = result.scalar_one_or_none()

        if not rate_limit:
            return {
                "used": 0,
                "limit": STUDENT_DAILY_LIMIT,
                "remaining": STUDENT_DAILY_LIMIT,
                "reset_at": None,
                "is_limited": False,
            }

        reset_at = rate_limit.window_start + timedelta(hours=24)

        return {
            "used": rate_limit.message_count,
            "limit": STUDENT_DAILY_LIMIT,
            "remaining": max(0, STUDENT_DAILY_LIMIT - rate_limit.message_count),
            "reset_at": reset_at.isoformat(),
            "is_limited": rate_limit.is_limited,
        }
