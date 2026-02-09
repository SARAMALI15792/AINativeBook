"""Content management schemas for request/response validation."""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class ContentBase(BaseModel):
    """Base content fields."""
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    content_type: str = Field(..., pattern="^(lesson|exercise|simulation|resource)$")
    learning_objectives: List[str] = []
    order_index: int = Field(..., ge=0)
    mdx_path: str


class ContentCreate(ContentBase):
    """Create new content."""
    stage_id: str


class ContentUpdate(BaseModel):
    """Update existing content."""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    content_type: Optional[str] = None
    learning_objectives: Optional[List[str]] = None
    order_index: Optional[int] = None
    mdx_path: Optional[str] = None
    change_summary: str = Field(..., min_length=1)  # Required for versioning


class ContentResponse(ContentBase):
    """Content response."""
    id: str
    stage_id: str
    version_number: str
    review_status: str
    created_by: str
    created_at: datetime
    updated_at: datetime
    published_at: Optional[datetime]

    model_config = {"from_attributes": True}


class ContentVersionResponse(BaseModel):
    """Content version response."""
    id: str
    content_id: str
    version_number: str
    change_summary: str
    created_by: str
    created_at: datetime
    reviewed_by: Optional[str]
    reviewed_at: Optional[datetime]

    model_config = {"from_attributes": True}


class ContentReviewCreate(BaseModel):
    """Submit content for review."""
    content_id: str
    version_id: Optional[str] = None  # If None, review latest version


class ContentReviewUpdate(BaseModel):
    """Review decision."""
    status: str = Field(..., pattern="^(approved|rejected|changes_requested)$")
    comments: Optional[str] = None
    rating: Optional[int] = Field(None, ge=1, le=5)


class ContentReviewResponse(BaseModel):
    """Review response."""
    id: str
    content_id: str
    version_id: str
    reviewer_id: str
    status: str
    comments: Optional[str]
    rating: Optional[int]
    requested_at: datetime
    reviewed_at: Optional[datetime]

    model_config = {"from_attributes": True}


class ContentListResponse(BaseModel):
    """Paginated content list."""
    items: List[ContentResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
