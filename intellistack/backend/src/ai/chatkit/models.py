"""SQLAlchemy models for ChatKit conversation persistence."""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, Text, DateTime, Integer, ForeignKey, JSON, Boolean, Index
from sqlalchemy.orm import relationship
from src.shared.database import Base


class ChatKitThread(Base):
    """Represents a conversation thread between a user and the AI tutor."""

    __tablename__ = "chatkit_thread"

    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey("user.id"), nullable=False, index=True)
    course_id = Column(String(36), nullable=True, index=True)  # Associated course/stage
    lesson_stage = Column(Integer, nullable=True)  # Learning stage (1-5)
    title = Column(String(255), nullable=True)  # Auto-generated or user-provided
    status = Column(String(20), default="active", nullable=False)  # active, archived
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    enrollment_ended_at = Column(DateTime, nullable=True)  # For retention policy
    metadata = Column(JSON, nullable=True)  # Additional context (page URL, tags, etc.)

    # Relationship
    items = relationship("ChatKitThreadItem", back_populates="thread", cascade="all, delete-orphan")

    __table_args__ = (Index("ix_chatkit_thread_user_id", "user_id"),)


class ChatKitThreadItem(Base):
    """Represents a single message in a ChatKit conversation thread."""

    __tablename__ = "chatkit_thread_item"

    id = Column(String(36), primary_key=True)
    thread_id = Column(String(36), ForeignKey("chatkit_thread.id"), nullable=False, index=True)
    role = Column(String(20), nullable=False)  # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    metadata = Column(JSON, nullable=True)  # Message metadata (page context, token count, etc.)

    # Relationship
    thread = relationship("ChatKitThread", back_populates="items")

    __table_args__ = (Index("ix_chatkit_thread_item_thread_id", "thread_id"),)


class ChatKitRateLimit(Base):
    """Track message rate limiting per user (20 messages/day for students)."""

    __tablename__ = "chatkit_rate_limit"

    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey("user.id"), nullable=False, unique=True, index=True)
    message_count = Column(Integer, default=0, nullable=False)
    window_start = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_reset = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_limited = Column(Boolean, default=False, nullable=False)


class AiUsageMetric(Base):
    """Track AI tutor usage metrics for cost monitoring and analytics."""

    __tablename__ = "ai_usage_metric"

    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey("user.id"), nullable=False, index=True)
    message_count = Column(Integer, default=0, nullable=False)
    total_tokens = Column(Integer, default=0, nullable=False)
    input_tokens = Column(Integer, default=0, nullable=False)
    output_tokens = Column(Integer, default=0, nullable=False)
    average_response_time_ms = Column(Integer, default=0, nullable=False)
    error_count = Column(Integer, default=0, nullable=False)
    date = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)


class AuthEventLog(Base):
    """Log all authentication events for security and auditing."""

    __tablename__ = "auth_event_log"

    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), nullable=True, index=True)  # Nullable for events before account creation
    event_type = Column(String(50), nullable=False, index=True)  # login_success, login_failed, register, logout, password_reset, oauth_link, oauth_unlink
    email = Column(String(255), nullable=True)
    ip_address = Column(String(45), nullable=True)  # Supports IPv4 and IPv6
    user_agent = Column(Text, nullable=True)
    reason = Column(String(255), nullable=True)  # For failed attempts: wrong_password, account_locked, etc.
    metadata = Column(JSON, nullable=True)  # Additional event data
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    __table_args__ = (
        Index("ix_auth_event_log_user_id", "user_id"),
        Index("ix_auth_event_log_event_type", "event_type"),
        Index("ix_auth_event_log_created_at", "created_at"),
    )
