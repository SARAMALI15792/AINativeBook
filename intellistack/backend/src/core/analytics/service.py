"""Analytics service for data aggregation and reporting."""

from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any

from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.analytics.models import AnalyticsEvent, CohortAnalytics, InstitutionAnalytics
from src.core.institution.models import Cohort, CohortEnrollment, Institution


async def track_event(
    db: AsyncSession,
    event_type: str,
    event_category: str,
    user_id: Optional[str] = None,
    institution_id: Optional[str] = None,
    cohort_id: Optional[str] = None,
    event_data: Optional[Dict[str, Any]] = None,
    session_id: Optional[str] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
) -> None:
    """
    Track an analytics event.

    Args:
        db: Database session
        event_type: Type of event (e.g., 'content_viewed', 'badge_earned')
        event_category: Category (e.g., 'learning', 'community', 'admin')
        user_id: Optional user ID
        institution_id: Optional institution ID
        cohort_id: Optional cohort ID
        event_data: Optional event metadata
        session_id: Optional session ID
        ip_address: Optional IP address
        user_agent: Optional user agent
    """
    event = AnalyticsEvent(
        user_id=user_id,
        institution_id=institution_id,
        cohort_id=cohort_id,
        event_type=event_type,
        event_category=event_category,
        event_data=event_data or {},
        session_id=session_id,
        ip_address=ip_address,
        user_agent=user_agent,
    )

    db.add(event)
    await db.commit()


async def get_user_activity(
    db: AsyncSession,
    user_id: str,
    days: int = 30,
) -> Dict[str, Any]:
    """
    Get user activity summary.

    Args:
        db: Database session
        user_id: User ID
        days: Number of days to look back

    Returns:
        Dict with activity metrics
    """
    since = datetime.now(timezone.utc) - timedelta(days=days)

    # Count events by type
    result = await db.execute(
        select(
            AnalyticsEvent.event_type,
            func.count().label('count')
        )
        .where(
            and_(
                AnalyticsEvent.user_id == user_id,
                AnalyticsEvent.created_at >= since,
            )
        )
        .group_by(AnalyticsEvent.event_type)
    )

    events_by_type = {row[0]: row[1] for row in result.all()}

    return {
        'user_id': user_id,
        'period_days': days,
        'events_by_type': events_by_type,
        'total_events': sum(events_by_type.values()),
    }


async def get_cohort_activity_summary(
    db: AsyncSession,
    cohort_id: str,
) -> Dict[str, Any]:
    """
    Get cohort activity summary.

    Args:
        db: Database session
        cohort_id: Cohort ID

    Returns:
        Dict with cohort metrics
    """
    # Get enrollment count
    enrollment_result = await db.execute(
        select(func.count()).where(
            and_(
                CohortEnrollment.cohort_id == cohort_id,
                CohortEnrollment.dropped_at.is_(None),
            )
        )
    )
    total_enrollments = enrollment_result.scalar() or 0

    # Get recent events (last 7 days)
    since = datetime.now(timezone.utc) - timedelta(days=7)
    event_result = await db.execute(
        select(func.count()).where(
            and_(
                AnalyticsEvent.cohort_id == cohort_id,
                AnalyticsEvent.created_at >= since,
            )
        )
    )
    recent_events = event_result.scalar() or 0

    return {
        'cohort_id': cohort_id,
        'total_enrollments': total_enrollments,
        'recent_events_7d': recent_events,
    }
