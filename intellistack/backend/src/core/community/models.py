"""Community management models for forums, study groups, and mentorship (FR-053 to FR-058)."""

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Optional
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.shared.database import Base

if TYPE_CHECKING:
    from src.core.auth.models import User


class PostStatus(str, Enum):
    """Post visibility status."""

    PUBLISHED = "published"
    DRAFT = "draft"
    ARCHIVED = "archived"
    DELETED = "deleted"  # Soft delete


class ModerationAction(str, Enum):
    """Moderation action types."""

    FLAGGED = "flagged"
    REVIEWED = "reviewed"
    APPROVED = "approved"
    HIDDEN = "hidden"
    REMOVED = "removed"
    WARNED = "warned"
    SUSPENDED = "suspended"


class ForumCategory(Base):
    """
    Forum category organizing discussion topics.

    Examples: Q&A, Announcements, Project Showcase, Peer Review
    """

    __tablename__ = "forum_categories"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    icon: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    order_index: Mapped[int] = mapped_column(Integer, default=0)

    # Moderation settings
    requires_approval: Mapped[bool] = mapped_column(Boolean, default=False)
    allow_anonymous: Mapped[bool] = mapped_column(Boolean, default=False)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    threads: Mapped[list["ForumThread"]] = relationship(
        "ForumThread", back_populates="category"
    )


class ForumThread(Base):
    """
    Forum discussion thread.

    Supports nested replies with threading.
    """

    __tablename__ = "forum_threads"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
    )
    category_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("forum_categories.id"), nullable=False, index=True
    )
    author_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("users.id"), nullable=False, index=True
    )

    # Content
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[PostStatus] = mapped_column(String(20), default=PostStatus.PUBLISHED)

    # Metadata
    is_pinned: Mapped[bool] = mapped_column(Boolean, default=False)
    is_locked: Mapped[bool] = mapped_column(Boolean, default=False)
    reply_count: Mapped[int] = mapped_column(Integer, default=0, index=True)
    view_count: Mapped[int] = mapped_column(Integer, default=0)
    last_activity_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Stage context (for filtered discussions)
    stage_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=False), ForeignKey("stages.id"), nullable=True
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Relationships
    category: Mapped["ForumCategory"] = relationship("ForumCategory", back_populates="threads")
    author: Mapped["User"] = relationship("User", foreign_keys=[author_id])
    posts: Mapped[list["ForumPost"]] = relationship("ForumPost", back_populates="thread")
    reactions: Mapped[list["ForumReaction"]] = relationship("ForumReaction", back_populates="thread")


class ForumPost(Base):
    """
    Reply within a forum thread.

    Supports nested comments with parent_post_id for threading.
    """

    __tablename__ = "forum_posts"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
    )
    thread_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("forum_threads.id"), nullable=False, index=True
    )
    parent_post_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=False), ForeignKey("forum_posts.id"), nullable=True
    )
    author_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("users.id"), nullable=False, index=True
    )

    # Content
    content: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[PostStatus] = mapped_column(String(20), default=PostStatus.PUBLISHED)

    # Moderation
    is_answer: Mapped[bool] = mapped_column(Boolean, default=False)  # Marked as solution
    moderation_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Relationships
    thread: Mapped["ForumThread"] = relationship("ForumThread", back_populates="posts")
    author: Mapped["User"] = relationship("User", foreign_keys=[author_id])
    parent_post: Mapped[Optional["ForumPost"]] = relationship(
        "ForumPost", remote_side=[id], foreign_keys=[parent_post_id]
    )
    reactions: Mapped[list["ForumReaction"]] = relationship("ForumReaction", back_populates="post")


class ForumReaction(Base):
    """Emoji reactions on threads and posts (likes, helpful, etc.)."""

    __tablename__ = "forum_reactions"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
    )
    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("users.id"), nullable=False, index=True
    )

    # Target
    thread_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=False), ForeignKey("forum_threads.id"), nullable=True, index=True
    )
    post_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=False), ForeignKey("forum_posts.id"), nullable=True, index=True
    )

    # Reaction type
    reaction_type: Mapped[str] = mapped_column(String(50), nullable=False)  # "👍", "❤️", "😂", etc.

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationships
    user: Mapped["User"] = relationship("User")
    thread: Mapped[Optional["ForumThread"]] = relationship("ForumThread", back_populates="reactions")
    post: Mapped[Optional["ForumPost"]] = relationship("ForumPost", back_populates="reactions")


class StudyGroup(Base):
    """
    Self-organized study groups for collaboration (FR-054).

    Students form groups to work on content together.
    """

    __tablename__ = "study_groups"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
    )
    creator_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("users.id"), nullable=False
    )

    # Group info
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    stage_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=False), ForeignKey("stages.id"), nullable=True
    )

    # Settings
    max_members: Mapped[int] = mapped_column(Integer, default=10)
    is_open: Mapped[bool] = mapped_column(Boolean, default=True)
    settings: Mapped[dict] = mapped_column(JSONB, default=dict)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    creator: Mapped["User"] = relationship("User", foreign_keys=[creator_id])
    members: Mapped[list["StudyGroupMember"]] = relationship(
        "StudyGroupMember", back_populates="study_group"
    )


class StudyGroupMember(Base):
    """Membership in a study group with role."""

    __tablename__ = "study_group_members"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
    )
    study_group_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("study_groups.id"), nullable=False, index=True
    )
    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("users.id"), nullable=False, index=True
    )

    # Role in group
    role: Mapped[str] = mapped_column(
        String(50), nullable=False, default="member"
    )  # member, moderator

    # Timestamps
    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    left_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Relationships
    study_group: Mapped["StudyGroup"] = relationship("StudyGroup", back_populates="members")
    user: Mapped["User"] = relationship("User")


class Mentorship(Base):
    """
    Mentorship relationship between experienced and learning students (FR-055).

    Handles matching and tracking of mentor-mentee relationships.
    """

    __tablename__ = "mentorships"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
    )
    mentor_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("users.id"), nullable=False, index=True
    )
    mentee_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("users.id"), nullable=False, index=True
    )

    # Matching criteria
    stage_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=False), ForeignKey("stages.id"), nullable=True
    )
    compatibility_score: Mapped[float] = mapped_column(
        default=0.0
    )  # 0-100, based on interests/availability

    # Relationship status
    status: Mapped[str] = mapped_column(
        String(50), default="active"
    )  # active, inactive, completed, rejected
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    ended_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Metadata
    messages_count: Mapped[int] = mapped_column(Integer, default=0)
    last_interaction_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    mentor: Mapped["User"] = relationship("User", foreign_keys=[mentor_id])
    mentee: Mapped["User"] = relationship("User", foreign_keys=[mentee_id])


class ModerationRecord(Base):
    """
    Moderation actions on community content (FR-056).

    Audit trail for community management.
    """

    __tablename__ = "moderation_records"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
    )
    moderator_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("users.id"), nullable=False
    )

    # Target
    user_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=False), ForeignKey("users.id"), nullable=True
    )  # User being moderated
    thread_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=False), ForeignKey("forum_threads.id"), nullable=True
    )
    post_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=False), ForeignKey("forum_posts.id"), nullable=True
    )

    # Action
    action: Mapped[ModerationAction] = mapped_column(String(50), nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    metadata: Mapped[dict] = mapped_column(JSONB, default=dict)  # Context-specific data

    # Status
    status: Mapped[str] = mapped_column(String(50), default="active")
    resolved_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    moderator: Mapped["User"] = relationship("User", foreign_keys=[moderator_id])
    user: Mapped[Optional["User"]] = relationship("User", foreign_keys=[user_id])
