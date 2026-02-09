"""Institution management schemas for request/response validation."""

from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel, Field, HttpUrl


class InstitutionBase(BaseModel):
    """Base institution fields."""
    name: str = Field(..., min_length=2, max_length=255)
    institution_type: str = Field(..., pattern="^(university|college|bootcamp|corporate|self_paced)$")
    domain: Optional[str] = Field(None, max_length=255)
    logo_url: Optional[HttpUrl] = None
    primary_color: str = Field("#2e8555", pattern="^#[0-9a-fA-F]{6}$")
    secondary_color: Optional[str] = Field(None, pattern="^#[0-9a-fA-F]{6}$")
    welcome_message: Optional[str] = None
    webhook_url: Optional[HttpUrl] = None
    simulation_quota_hours: int = Field(25, ge=1, le=1000)


class InstitutionCreate(InstitutionBase):
    """Create new institution."""
    pass


class InstitutionUpdate(BaseModel):
    """Update institution."""
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    logo_url: Optional[HttpUrl] = None
    primary_color: Optional[str] = Field(None, pattern="^#[0-9a-fA-F]{6}$")
    secondary_color: Optional[str] = Field(None, pattern="^#[0-9a-fA-F]{6}$")
    welcome_message: Optional[str] = None
    webhook_url: Optional[HttpUrl] = None
    custom_css: Optional[str] = None
    settings: Optional[dict] = None


class InstitutionResponse(InstitutionBase):
    """Institution response."""
    id: str
    slug: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class CohortBase(BaseModel):
    """Base cohort fields."""
    name: str = Field(..., min_length=2, max_length=255)
    description: Optional[str] = None
    start_date: date
    end_date: date
    enrollment_limit: Optional[int] = Field(None, ge=1)
    is_enrollment_open: bool = True


class CohortCreate(CohortBase):
    """Create new cohort."""
    institution_id: str


class CohortUpdate(BaseModel):
    """Update cohort."""
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    enrollment_limit: Optional[int] = None
    is_enrollment_open: Optional[bool] = None


class CohortResponse(CohortBase):
    """Cohort response."""
    id: str
    institution_id: str
    created_by: str
    created_at: datetime
    enrolled_count: int = 0

    model_config = {"from_attributes": True}


class EnrollmentCreate(BaseModel):
    """Enroll student in cohort."""
    cohort_id: str
    user_id: str


class EnrollmentResponse(BaseModel):
    """Enrollment response."""
    id: str
    cohort_id: str
    user_id: str
    enrolled_at: datetime
    enrolled_by: Optional[str]

    model_config = {"from_attributes": True}


class InstructorAssignment(BaseModel):
    """Assign instructor to cohort."""
    cohort_id: str
    user_id: str


class CohortAnalyticsResponse(BaseModel):
    """Cohort analytics."""
    cohort_id: str
    total_students: int
    active_students: int
    completed_students: int
    average_progress_percentage: float
    average_stage: float
    total_badges_earned: int
    total_time_spent_hours: float
    daily_active_users: int
    last_updated: datetime

    model_config = {"from_attributes": True}


class InstitutionAnalyticsResponse(BaseModel):
    """Institution-wide analytics."""
    institution_id: str
    total_cohorts: int
    active_cohorts: int
    total_students: int
    active_students: int
    completed_students: int
    average_progress_percentage: float
    total_badges_earned: int
    total_certificates_issued: int
    total_time_spent_hours: float
    last_updated: datetime

    model_config = {"from_attributes": True}
