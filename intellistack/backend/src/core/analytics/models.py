"""Analytics models for tracking and reporting."""

from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.shared.database import Base


class AnalyticsEvent(Base):
    """
    Generic analytics event tracking.

    Stores user actions for analysis and reporting.
    """

    __tablename__ = "analytics_events"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
    )
    user_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=False), ForeignKey("users.id"), nullable=True, index=True
    )
    institution_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=False), ForeignKey("institutions.id"), nullable=True, index=True
    )
    cohort_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=False), ForeignKey("cohorts.id"), nullable=True, index=True
    )

    # Event details
    event_type: Mapped[str] = mapped_column(
        String(100), nullable=False, index=True
    )  # content_viewed, assessment_completed, etc.
    event_category: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # learning, community, admin, etc.
    event_data: Mapped[dict] = mapped_column(JSONB, default=dict)

    # Session tracking
    session_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Timestamp
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), index=True
    )


class CohortAnalytics(Base):
    """
    Aggregated analytics per cohort.

    Pre-computed metrics for dashboard performance.
    """

    __tablename__ = "cohort_analytics"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
    )
    cohort_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("cohorts.id"), nullable=False, unique=True, index=True
    )

    # Student metrics
    total_students: Mapped[int] = mapped_column(Integer, default=0)
    active_students: Mapped[int] = mapped_column(Integer, default=0)
    completed_students: Mapped[int] = mapped_column(Integer, default=0)

    # Progress metrics
    average_progress_percentage: Mapped[float] = mapped_column(Float, default=0.0)
    average_stage: Mapped[float] = mapped_column(Float, default=1.0)
    total_badges_earned: Mapped[int] = mapped_column(Integer, default=0)
    total_certificates_issued: Mapped[int] = mapped_column(Integer, default=0)

    # Engagement metrics
    total_time_spent_hours: Mapped[float] = mapped_column(Float, default=0.0)
    average_time_per_student: Mapped[float] = mapped_column(Float, default=0.0)
    total_assessments_taken: Mapped[int] = mapped_column(Integer, default=0)
    average_assessment_score: Mapped[float] = mapped_column(Float, default=0.0)

    # Activity metrics
    daily_active_users: Mapped[int] = mapped_column(Integer, default=0)
    weekly_active_users: Mapped[int] = mapped_column(Integer, default=0)
    monthly_active_users: Mapped[int] = mapped_column(Integer, default=0)

    # Last updated
    last_updated: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    cohort: Mapped["Cohort"] = relationship("Cohort")


class InstitutionAnalytics(Base):
    """
    Aggregated analytics per institution.

    Institution-wide metrics for administrators.
    """

    __tablename__ = "institution_analytics"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
    )
    institution_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("institutions.id"), nullable=False, unique=True, index=True
    )

    # Cohort metrics
    total_cohorts: Mapped[int] = mapped_column(Integer, default=0)
    active_cohorts: Mapped[int] = mapped_column(Integer, default=0)

    # Student metrics (across all cohorts)
    total_students: Mapped[int] = mapped_column(Integer, default=0)
    active_students: Mapped[int] = mapped_column(Integer, default=0)
    completed_students: Mapped[int] = mapped_column(Integer, default=0)

    # Progress metrics
    average_progress_percentage: Mapped[float] = mapped_column(Float, default=0.0)
    total_badges_earned: Mapped[int] = mapped_column(Integer, default=0)
    total_certificates_issued: Mapped[int] = mapped_column(Integer, default=0)

    # Engagement metrics
    total_time_spent_hours: Mapped[float] = mapped_column(Float, default=0.0)
    average_session_duration_minutes: Mapped[float] = mapped_column(Float, default=0.0)

    # Content metrics
    total_content_created: Mapped[int] = mapped_column(Integer, default=0)
    total_content_published: Mapped[int] = mapped_column(Integer, default=0)

    # Last updated
    last_updated: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    institution: Mapped["Institution"] = relationship("Institution")
