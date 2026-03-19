"""Pydantic schemas for community API."""

from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field


class ForumCategoryResponse(BaseModel):
    """Forum category response."""

    id: str
    name: str
    description: Optional[str]
    icon: Optional[str]
    requires_approval: bool
    allow_anonymous: bool
    order_index: int

    class Config:
        from_attributes = True


class ForumThreadCreate(BaseModel):
    """Create forum thread."""

    category_id: str
    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)
    stage_id: Optional[str] = None


class ForumThreadUpdate(BaseModel):
    """Update forum thread."""

    title: Optional[str] = None
    content: Optional[str] = None
    is_pinned: Optional[bool] = None
    is_locked: Optional[bool] = None


class ForumThreadResponse(BaseModel):
    """Forum thread response."""

    id: str
    category_id: str
    title: str
    content: str
    author_id: str
    status: str
    is_pinned: bool
    is_locked: bool
    reply_count: int
    view_count: int
    stage_id: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ForumPostCreate(BaseModel):
    """Create forum post (reply)."""

    thread_id: str
    content: str = Field(..., min_length=1)
    parent_post_id: Optional[str] = None


class ForumPostResponse(BaseModel):
    """Forum post response."""

    id: str
    thread_id: str
    author_id: str
    content: str
    status: str
    is_answer: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class StudyGroupCreate(BaseModel):
    """Create study group."""

    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    stage_id: Optional[str] = None
    max_members: int = Field(default=10, ge=2, le=50)


class StudyGroupResponse(BaseModel):
    """Study group response."""

    id: str
    creator_id: str
    name: str
    description: Optional[str]
    stage_id: Optional[str]
    max_members: int
    is_open: bool
    created_at: datetime
    member_count: int

    class Config:
        from_attributes = True


class MentorshipResponse(BaseModel):
    """Mentorship response."""

    id: str
    mentor_id: str
    mentee_id: str
    stage_id: Optional[str]
    compatibility_score: float
    status: str
    started_at: datetime
    messages_count: int

    class Config:
        from_attributes = True


class ModerationActionCreate(BaseModel):
    """Create moderation action."""

    action: str
    reason: str
    user_id: Optional[str] = None
    thread_id: Optional[str] = None
    post_id: Optional[str] = None


class NotificationCreate(BaseModel):
    """Create notification."""

    user_id: str
    event_type: str  # reply, mention, moderation, etc.
    title: str
    message: str
    related_object_id: Optional[str] = None
    related_object_type: Optional[str] = None
