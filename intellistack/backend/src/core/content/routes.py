"""Content management API routes."""

from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth.models import User
from src.core.auth.dependencies import get_current_active_user
from src.core.content import service
from src.core.content.schemas import (
    ContentCreate,
    ContentUpdate,
    ContentResponse,
    ContentVersionResponse,
    ContentReviewCreate,
    ContentReviewUpdate,
    ContentReviewResponse,
    ContentListResponse,
)
from src.shared.database import get_session
from src.shared.middleware import require_role

router = APIRouter(prefix="/content", tags=["content"])


@router.post("/", response_model=ContentResponse, status_code=status.HTTP_201_CREATED)
async def create_content_item(
    content_data: ContentCreate,
    db: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """
    Create new content item (authors only).

    Args:
        content_data: Content creation data
        current_user: Current authenticated user
        db: Database session

    Returns:
        ContentResponse: Created content
    """
    # TODO: Use @require_role("author") decorator
    return await service.create_content(db, content_data, str(current_user.id))


@router.get("/", response_model=ContentListResponse)
async def list_content_items(
    db: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    stage_id: Optional[str] = Query(None, description="Filter by stage ID"),
    status_filter: Optional[str] = Query(None, alias="status", description="Filter by status"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
):
    """
    List content items with pagination.

    Args:
        stage_id: Optional stage filter
        status_filter: Optional status filter
        page: Page number
        page_size: Items per page
        db: Database session
        current_user: Current authenticated user

    Returns:
        ContentListResponse: Paginated content list
    """
    from src.core.content.models import ContentStatus

    status_enum = ContentStatus(status_filter) if status_filter else None
    return await service.list_content(db, stage_id, status_enum, page, page_size)


@router.get("/{content_id}", response_model=ContentResponse)
async def get_content_item(
    content_id: str,
    db: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """
    Get content item by ID.

    Args:
        content_id: Content ID
        db: Database session
        current_user: Current authenticated user

    Returns:
        ContentResponse: Content details

    Raises:
        HTTPException: If content not found
    """
    from sqlalchemy import select
    from src.core.content.models import Content

    result = await db.execute(select(Content).where(Content.id == content_id))
    content = result.scalar_one_or_none()

    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    return ContentResponse.model_validate(content)


@router.put("/{content_id}", response_model=ContentResponse)
async def update_content_item(
    content_id: str,
    update_data: ContentUpdate,
    db: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """
    Update content item (creates new version).

    Args:
        content_id: Content ID
        update_data: Update data
        current_user: Current authenticated user
        db: Database session

    Returns:
        ContentResponse: Updated content
    """
    return await service.update_content(db, content_id, update_data, str(current_user.id))


@router.post("/{content_id}/submit", response_model=ContentResponse)
async def submit_content_for_review(
    content_id: str,
    db: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """
    Submit content for review (FR-059).

    Args:
        content_id: Content ID
        current_user: Current authenticated user
        db: Database session

    Returns:
        ContentResponse: Content with updated status
    """
    return await service.submit_for_review(db, content_id)


@router.post("/{content_id}/review", response_model=ContentResponse)
async def review_content_item(
    content_id: str,
    review_data: ContentReviewUpdate,
    db: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """
    Review content (instructors/admins only).

    Args:
        content_id: Content ID
        review_data: Review decision
        current_user: Current authenticated user (must be instructor)
        db: Database session

    Returns:
        ContentResponse: Content with updated status
    """
    # TODO: Use @require_role("instructor", "platform_admin") decorator
    return await service.review_content(db, content_id, review_data, str(current_user.id))


@router.get("/{content_id}/versions", response_model=list[ContentVersionResponse])
async def get_content_versions(
    content_id: str,
    db: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """
    Get version history for content.

    Args:
        content_id: Content ID
        db: Database session
        current_user: Current authenticated user

    Returns:
        List of content versions
    """
    return await service.get_content_versions(db, content_id)


@router.delete("/{content_id}", status_code=status.HTTP_204_NO_CONTENT)
async def archive_content_item(
    content_id: str,
    db: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """
    Archive content (soft delete).

    Args:
        content_id: Content ID
        current_user: Current authenticated user
        db: Database session
    """
    await service.archive_content(db, content_id)
