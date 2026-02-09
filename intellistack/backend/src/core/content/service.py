"""Content management service with versioning and review workflow."""

import hashlib
from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status

from src.core.content.models import (
    Content,
    ContentVersion,
    ContentReview,
    ContentStatus,
    ReviewStatus,
)
from src.core.content.schemas import (
    ContentCreate,
    ContentUpdate,
    ContentResponse,
    ContentVersionResponse,
    ContentReviewUpdate,
    ContentListResponse,
)


async def create_content(
    db: AsyncSession,
    content_data: ContentCreate,
    author_id: str,
) -> ContentResponse:
    """
    Create new content item.

    Args:
        db: Database session
        content_data: Content creation data
        author_id: Author user ID

    Returns:
        ContentResponse: Created content
    """
    # Create content
    new_content = Content(
        stage_id=content_data.stage_id,
        content_type=content_data.content_type,
        title=content_data.title,
        description=content_data.description,
        learning_objectives=content_data.learning_objectives,
        order_index=content_data.order_index,
        mdx_path=content_data.mdx_path,
        created_by=author_id,
        review_status=ContentStatus.DRAFT,
    )

    db.add(new_content)
    await db.flush()

    # Create initial version
    version = await _create_version(
        db,
        content_id=new_content.id,
        title=content_data.title,
        content_json={
            "title": content_data.title,
            "description": content_data.description,
            "mdx_path": content_data.mdx_path,
        },
        mdx_hash="initial",  # TODO: Calculate actual hash
        change_summary="Initial version",
        author_id=author_id,
    )

    new_content.current_version_id = version.id
    await db.commit()
    await db.refresh(new_content)

    return ContentResponse.model_validate(new_content)


async def update_content(
    db: AsyncSession,
    content_id: str,
    update_data: ContentUpdate,
    author_id: str,
) -> ContentResponse:
    """
    Update content and create new version (FR-060).

    Args:
        db: Database session
        content_id: Content ID to update
        update_data: Update data
        author_id: Author user ID

    Returns:
        ContentResponse: Updated content

    Raises:
        HTTPException: If content not found
    """
    # Find content
    result = await db.execute(select(Content).where(Content.id == content_id))
    content = result.scalar_one_or_none()

    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    # Update fields
    if update_data.title:
        content.title = update_data.title
    if update_data.description is not None:
        content.description = update_data.description
    if update_data.content_type:
        content.content_type = update_data.content_type
    if update_data.learning_objectives is not None:
        content.learning_objectives = update_data.learning_objectives
    if update_data.order_index is not None:
        content.order_index = update_data.order_index
    if update_data.mdx_path:
        content.mdx_path = update_data.mdx_path

    content.updated_by = author_id

    # Create new version
    version = await _create_version(
        db,
        content_id=content.id,
        title=content.title,
        content_json={
            "title": content.title,
            "description": content.description,
            "mdx_path": content.mdx_path,
        },
        mdx_hash="updated",  # TODO: Calculate actual hash
        change_summary=update_data.change_summary,
        author_id=author_id,
    )

    # Increment version number
    major, minor, patch = content.version_number.split(".")
    content.version_number = f"{major}.{minor}.{int(patch) + 1}"
    content.current_version_id = version.id

    # Reset review status to draft if published
    if content.review_status == ContentStatus.PUBLISHED:
        content.review_status = ContentStatus.DRAFT

    await db.commit()
    await db.refresh(content)

    return ContentResponse.model_validate(content)


async def submit_for_review(
    db: AsyncSession,
    content_id: str,
) -> ContentResponse:
    """
    Submit content for review.

    Args:
        db: Database session
        content_id: Content ID

    Returns:
        ContentResponse: Updated content

    Raises:
        HTTPException: If content not found or already in review
    """
    result = await db.execute(select(Content).where(Content.id == content_id))
    content = result.scalar_one_or_none()

    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    if content.review_status != ContentStatus.DRAFT:
        raise HTTPException(
            status_code=400,
            detail=f"Content must be in draft status to submit for review (current: {content.review_status})",
        )

    content.review_status = ContentStatus.IN_REVIEW
    await db.commit()
    await db.refresh(content)

    return ContentResponse.model_validate(content)


async def review_content(
    db: AsyncSession,
    content_id: str,
    review_data: ContentReviewUpdate,
    reviewer_id: str,
) -> ContentResponse:
    """
    Review content and update status.

    Args:
        db: Database session
        content_id: Content ID
        review_data: Review decision
        reviewer_id: Reviewer user ID

    Returns:
        ContentResponse: Updated content

    Raises:
        HTTPException: If content not found or not in review
    """
    result = await db.execute(
        select(Content).options(selectinload(Content.versions)).where(Content.id == content_id)
    )
    content = result.scalar_one_or_none()

    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    if content.review_status != ContentStatus.IN_REVIEW:
        raise HTTPException(status_code=400, detail="Content not in review status")

    # Create review record
    review = ContentReview(
        content_id=content.id,
        version_id=content.current_version_id,
        reviewer_id=reviewer_id,
        status=ReviewStatus[review_data.status.upper()],
        comments=review_data.comments,
        rating=review_data.rating,
        reviewed_at=datetime.now(timezone.utc),
    )
    db.add(review)

    # Update content status based on review
    if review_data.status == "approved":
        content.review_status = ContentStatus.PUBLISHED
        content.published_at = datetime.now(timezone.utc)

        # Update version reviewed fields
        if content.current_version_id:
            version_result = await db.execute(
                select(ContentVersion).where(ContentVersion.id == content.current_version_id)
            )
            version = version_result.scalar_one_or_none()
            if version:
                version.reviewed_by = reviewer_id
                version.reviewed_at = datetime.now(timezone.utc)

    elif review_data.status in ["rejected", "changes_requested"]:
        content.review_status = ContentStatus.DRAFT

    await db.commit()
    await db.refresh(content)

    # TODO: Send notification to author (FR-009)

    return ContentResponse.model_validate(content)


async def list_content(
    db: AsyncSession,
    stage_id: Optional[str] = None,
    status: Optional[ContentStatus] = None,
    page: int = 1,
    page_size: int = 20,
) -> ContentListResponse:
    """
    List content with pagination and filtering.

    Args:
        db: Database session
        stage_id: Filter by stage
        status: Filter by review status
        page: Page number (1-indexed)
        page_size: Items per page

    Returns:
        ContentListResponse: Paginated content list
    """
    # Build query
    query = select(Content)

    if stage_id:
        query = query.where(Content.stage_id == stage_id)
    if status:
        query = query.where(Content.review_status == status)

    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()

    # Paginate
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size).order_by(Content.order_index)

    result = await db.execute(query)
    items = result.scalars().all()

    return ContentListResponse(
        items=[ContentResponse.model_validate(item) for item in items],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )


async def get_content_versions(
    db: AsyncSession,
    content_id: str,
) -> List[ContentVersionResponse]:
    """
    Get version history for content.

    Args:
        db: Database session
        content_id: Content ID

    Returns:
        List of content versions
    """
    result = await db.execute(
        select(ContentVersion)
        .where(ContentVersion.content_id == content_id)
        .order_by(ContentVersion.created_at.desc())
    )
    versions = result.scalars().all()

    return [ContentVersionResponse.model_validate(v) for v in versions]


async def _create_version(
    db: AsyncSession,
    content_id: str,
    title: str,
    content_json: dict,
    mdx_hash: str,
    change_summary: str,
    author_id: str,
) -> ContentVersion:
    """
    Internal helper to create a content version.

    Args:
        db: Database session
        content_id: Parent content ID
        title: Version title
        content_json: Content snapshot
        mdx_hash: Hash of MDX file
        change_summary: Change description
        author_id: Author user ID

    Returns:
        Created ContentVersion
    """
    # Get current version count
    result = await db.execute(
        select(func.count()).where(ContentVersion.content_id == content_id)
    )
    version_count = result.scalar() or 0

    # Generate version number
    version_number = f"1.0.{version_count}"

    version = ContentVersion(
        content_id=content_id,
        version_number=version_number,
        title=title,
        content_json=content_json,
        mdx_content_hash=mdx_hash,
        change_summary=change_summary,
        created_by=author_id,
    )

    db.add(version)
    await db.flush()

    return version


async def archive_content(
    db: AsyncSession,
    content_id: str,
) -> ContentResponse:
    """
    Archive content (soft delete).

    Args:
        db: Database session
        content_id: Content ID

    Returns:
        ContentResponse: Archived content
    """
    result = await db.execute(select(Content).where(Content.id == content_id))
    content = result.scalar_one_or_none()

    if not content:
        raise HTTPException(status_code=404, detail="Content not found")

    content.review_status = ContentStatus.ARCHIVED
    await db.commit()
    await db.refresh(content)

    return ContentResponse.model_validate(content)
