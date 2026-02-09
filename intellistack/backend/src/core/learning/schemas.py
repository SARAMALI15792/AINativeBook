"""Pydantic schemas for Learning module API."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# === Stage Schemas ===


class StageBase(BaseModel):
    """Base stage schema."""

    name: str
    description: Optional[str] = None
    estimated_hours: int = 40


class StageResponse(BaseModel):
    """Stage response schema."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    number: int
    name: str
    slug: str
    description: Optional[str]
    learning_objectives: list[str]
    estimated_hours: int
    content_count: int
    prerequisite_stage_id: Optional[str]
    is_active: bool


class StageWithStatus(StageResponse):
    """Stage with user-specific status."""

    status: str  # locked, available, in_progress, completed
    percentage_complete: float = 0.0
    is_accessible: bool = False


# === Content Item Schemas ===


class ContentItemResponse(BaseModel):
    """Content item response schema."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    slug: str
    content_type: str
    order: int
    estimated_minutes: int
    is_required: bool
    is_completed: bool = False


# === Progress Schemas ===


class ProgressResponse(BaseModel):
    """User progress response schema."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    current_stage_id: Optional[str]
    overall_percentage: float
    total_time_spent_minutes: int
    stage_progress: dict
    started_at: datetime
    last_activity_at: datetime
    completed_at: Optional[datetime]


class StageProgressDetail(BaseModel):
    """Detailed progress for a single stage."""

    stage_id: str
    stage_number: int
    stage_name: str
    status: str
    percentage: float
    completed_items: int
    total_items: int
    started_at: Optional[datetime]
    completed_at: Optional[datetime]


class LearningPathResponse(BaseModel):
    """Learning path visualization response (FR-012)."""

    user_id: str
    overall_percentage: float
    current_stage: Optional[StageWithStatus]
    stages: list[StageWithStatus]
    total_badges_earned: int
    estimated_hours_remaining: int


# === Content Completion Schemas ===


class CompleteContentRequest(BaseModel):
    """Request to mark content as complete."""

    time_spent_minutes: int = Field(ge=0, default=0)
    score: Optional[float] = Field(ge=0, le=100, default=None)


class CompleteContentResponse(BaseModel):
    """Response after completing content."""

    content_id: str
    completed_at: datetime
    stage_percentage: float
    overall_percentage: float
    badge_earned: Optional[str] = None
    stage_completed: bool = False
    next_content_id: Optional[str] = None


# === Badge Schemas ===


class BadgeResponse(BaseModel):
    """Badge response schema."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    description: Optional[str]
    icon_url: Optional[str]
    stage_id: Optional[str]


class UserBadgeResponse(BaseModel):
    """User badge response schema."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    badge: BadgeResponse
    awarded_at: datetime
    awarded_for: Optional[str]


# === Certificate Schemas ===


class CertificateResponse(BaseModel):
    """Certificate response schema."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    certificate_number: str
    issued_at: datetime
    total_time_spent_hours: int
    final_assessment_score: Optional[float]
    verification_url: Optional[str]
    pdf_url: Optional[str]


# === Time Estimate Schemas ===


class TimeEstimateResponse(BaseModel):
    """Estimated time to completion (FR-007)."""

    stage_id: str
    estimated_hours_remaining: float
    based_on_user_pace: bool = False
    average_completion_rate: float = 1.0  # multiplier
