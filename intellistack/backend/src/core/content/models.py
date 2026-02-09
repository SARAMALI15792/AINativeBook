"""Content management models for versioning and review workflow."""

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Optional
from uuid import uuid4

from sqlalchemy import DateTime, Enum as SQLEnum, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.shared.database import Base

if TYPE_CHECKING:
    from src.core.auth.models import User

# Note: Using string reference for forward declaration
# from src.core.learning.models import Stage


class ContentStatus(str, Enum):
    """Content review status (FR-059)."""

    DRAFT = "draft"
    IN_REVIEW = "in_review"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class ReviewStatus(str, Enum):
    """Review decision status."""

    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CHANGES_REQUESTED = "changes_requested"


class Content(Base):
    """
    Content item with versioning support (FR-060).

    Represents a lesson, exercise, or resource in the learning platform.
    """

    __tablename__ = "content"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
    )
    stage_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("stages.id"), nullable=False, index=True
    )
    content_type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # lesson, exercise, simulation, resource
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    learning_objectives: Mapped[dict] = mapped_column(JSONB, nullable=False, default=list)
    order_index: Mapped[int] = mapped_column(Integer, nullable=False)

    # File references
    mdx_path: Mapped[str] = mapped_column(
        String(500), nullable=False
    )  # Path to MDX file in content repo
    format_variants: Mapped[dict] = mapped_column(
        JSONB, default=list
    )  # Available formats (video, text, interactive)

    # Versioning
    current_version_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=False), ForeignKey("content_versions.id"), nullable=True
    )
    version_number: Mapped[str] = mapped_column(
        String(20), default="1.0.0"
    )  # Semantic versioning

    # Status
    review_status: Mapped[ContentStatus] = mapped_column(
        SQLEnum(ContentStatus), nullable=False, default=ContentStatus.DRAFT, index=True
    )

    # Authorship
    created_by: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("users.id"), nullable=False
    )
    updated_by: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=False), ForeignKey("users.id"), nullable=True
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    published_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Relationships
    # Note: Stage relationship handled via foreign key only (avoid circular import)
    author: Mapped["User"] = relationship("User", foreign_keys=[created_by])
    versions: Mapped[list["ContentVersion"]] = relationship(
        "ContentVersion", back_populates="content", foreign_keys="ContentVersion.content_id"
    )
    reviews: Mapped[list["ContentReview"]] = relationship(
        "ContentReview", back_populates="content"
    )


class ContentVersion(Base):
    """
    Version history for content (FR-060).

    Each edit creates a new version, enabling rollback and change tracking.
    """

    __tablename__ = "content_versions"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
    )
    content_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("content.id"), nullable=False, index=True
    )
    version_number: Mapped[str] = mapped_column(String(20), nullable=False)
    change_summary: Mapped[str] = mapped_column(Text, nullable=False)

    # Content snapshot
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content_json: Mapped[dict] = mapped_column(
        JSONB, nullable=False
    )  # Full content snapshot including MDX
    mdx_content_hash: Mapped[str] = mapped_column(
        String(64), nullable=False
    )  # SHA-256 of MDX file

    # Authorship
    created_by: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("users.id"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), index=True
    )

    # Review
    reviewed_by: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=False), ForeignKey("users.id"), nullable=True
    )
    reviewed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Relationships
    content: Mapped["Content"] = relationship(
        "Content", back_populates="versions", foreign_keys=[content_id]
    )
    author: Mapped["User"] = relationship("User", foreign_keys=[created_by])
    reviewer: Mapped[Optional["User"]] = relationship("User", foreign_keys=[reviewed_by])


class ContentReview(Base):
    """
    Content review workflow (FR-059).

    Tracks review process for content before publication.
    """

    __tablename__ = "content_reviews"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
    )
    content_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("content.id"), nullable=False, index=True
    )
    version_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("content_versions.id"), nullable=False
    )
    reviewer_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("users.id"), nullable=False
    )

    # Review details
    status: Mapped[ReviewStatus] = mapped_column(
        SQLEnum(ReviewStatus), nullable=False, default=ReviewStatus.PENDING
    )
    comments: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    rating: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True
    )  # 1-5 quality rating

    # Timestamps
    requested_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    reviewed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Relationships
    content: Mapped["Content"] = relationship("Content", back_populates="reviews")
    version: Mapped["ContentVersion"] = relationship("ContentVersion")
    reviewer: Mapped["User"] = relationship("User")
