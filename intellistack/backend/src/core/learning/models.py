"""Learning management models - stages, progress, badges, certificates."""

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Optional
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.shared.database import Base

if TYPE_CHECKING:
    from src.core.auth.models import User


class StageStatus(str, Enum):
    """Stage completion status for a user."""

    LOCKED = "locked"
    AVAILABLE = "available"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Stage(Base):
    """Learning stage definition (5 stages per curriculum)."""

    __tablename__ = "stages"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
    )
    number: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    learning_objectives: Mapped[list] = mapped_column(JSONB, default=list)

    # Prerequisites - self-referential (FR-001)
    prerequisite_stage_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=False), ForeignKey("stages.id"), nullable=True
    )

    # Estimated time in hours
    estimated_hours: Mapped[int] = mapped_column(Integer, default=40)

    # Content metadata
    content_count: Mapped[int] = mapped_column(Integer, default=0)
    assessment_count: Mapped[int] = mapped_column(Integer, default=0)

    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationships
    prerequisite: Mapped[Optional["Stage"]] = relationship(
        "Stage", remote_side=[id], foreign_keys=[prerequisite_stage_id]
    )
    content_items: Mapped[list["ContentItem"]] = relationship(
        "ContentItem", back_populates="stage"
    )
    badges: Mapped[list["Badge"]] = relationship("Badge", back_populates="stage")


class ContentItem(Base):
    """Individual content piece within a stage."""

    __tablename__ = "content_items"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
    )
    stage_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("stages.id"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), nullable=False)
    content_type: Mapped[str] = mapped_column(String(50), default="lesson")  # lesson, exercise, quiz
    order: Mapped[int] = mapped_column(Integer, default=0)
    estimated_minutes: Mapped[int] = mapped_column(Integer, default=30)
    content_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    is_required: Mapped[bool] = mapped_column(Boolean, default=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationships
    stage: Mapped["Stage"] = relationship("Stage", back_populates="content_items")
    completions: Mapped[list["ContentCompletion"]] = relationship(
        "ContentCompletion", back_populates="content_item"
    )


class Badge(Base):
    """Achievement badge awarded for stage completion (FR-005)."""

    __tablename__ = "badges"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
    )
    stage_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=False), ForeignKey("stages.id"), nullable=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    icon_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    criteria: Mapped[dict] = mapped_column(JSONB, default=dict)  # JSON criteria for earning

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationships
    stage: Mapped[Optional["Stage"]] = relationship("Stage", back_populates="badges")
    user_badges: Mapped[list["UserBadge"]] = relationship("UserBadge", back_populates="badge")


class Progress(Base):
    """User's overall learning progress across all stages (FR-003)."""

    __tablename__ = "progress"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
    )
    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("users.id"), nullable=False, unique=True
    )

    # Current progress
    current_stage_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=False), ForeignKey("stages.id"), nullable=True
    )
    overall_percentage: Mapped[float] = mapped_column(Float, default=0.0)
    total_time_spent_minutes: Mapped[int] = mapped_column(Integer, default=0)

    # Stage-specific progress stored as JSON
    # Format: {"stage_id": {"percentage": 50.0, "status": "in_progress", "started_at": "..."}}
    stage_progress: Mapped[dict] = mapped_column(JSONB, default=dict)

    # Timestamps
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    last_activity_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="progress")
    current_stage: Mapped[Optional["Stage"]] = relationship("Stage")
    content_completions: Mapped[list["ContentCompletion"]] = relationship(
        "ContentCompletion", back_populates="progress"
    )


class ContentCompletion(Base):
    """Tracks individual content item completions for a user."""

    __tablename__ = "content_completions"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
    )
    progress_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("progress.id"), nullable=False
    )
    content_item_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("content_items.id"), nullable=False
    )

    # Completion details
    completed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    time_spent_minutes: Mapped[int] = mapped_column(Integer, default=0)
    score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # For assessments

    # Relationships
    progress: Mapped["Progress"] = relationship("Progress", back_populates="content_completions")
    content_item: Mapped["ContentItem"] = relationship(
        "ContentItem", back_populates="completions"
    )


class UserBadge(Base):
    """Badge awarded to a user."""

    __tablename__ = "user_badges"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
    )
    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("users.id"), nullable=False
    )
    badge_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("badges.id"), nullable=False
    )

    awarded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    awarded_for: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="badges")
    badge: Mapped["Badge"] = relationship("Badge", back_populates="user_badges")


class Certificate(Base):
    """Completion certificate for finishing all 5 stages (FR-014)."""

    __tablename__ = "certificates"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
    )
    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("users.id"), nullable=False
    )

    certificate_number: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True
    )
    issued_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Completion details
    total_time_spent_hours: Mapped[int] = mapped_column(Integer, default=0)
    final_assessment_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Verification
    verification_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    pdf_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
