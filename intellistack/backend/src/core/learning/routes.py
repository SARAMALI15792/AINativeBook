"""Learning API routes - stages, progress, badges, certificates."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.database import get_session
from src.shared.exceptions import IntelliStackError, NotFoundError, PrerequisiteNotMetError

from .schemas import (
    BadgeResponse,
    CertificateResponse,
    CompleteContentRequest,
    CompleteContentResponse,
    ContentItemResponse,
    LearningPathResponse,
    ProgressResponse,
    StageResponse,
    StageWithStatus,
    TimeEstimateResponse,
    UserBadgeResponse,
)
from .service import LearningService

router = APIRouter(prefix="/learning", tags=["Learning"])

# Dependency for session
SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_learning_service(session: SessionDep) -> LearningService:
    """Dependency to get learning service instance."""
    return LearningService(session)


ServiceDep = Annotated[LearningService, Depends(get_learning_service)]


# TODO: Replace with actual auth dependency
def get_current_user_id() -> str:
    """Temporary: Get current user ID (replace with auth)."""
    return "test-user-id"


CurrentUserDep = Annotated[str, Depends(get_current_user_id)]


# === Stage Endpoints ===


@router.get("/stages", response_model=list[StageResponse])
async def list_stages(service: ServiceDep) -> list[StageResponse]:
    """Get all learning stages.

    Returns the 5-stage curriculum overview without user-specific progress.
    """
    stages = await service.get_all_stages()
    return [StageResponse.model_validate(s) for s in stages]


@router.get("/stages/{stage_id}", response_model=StageWithStatus)
async def get_stage(
    stage_id: str,
    service: ServiceDep,
    user_id: CurrentUserDep,
) -> StageWithStatus:
    """Get a specific stage with user's status.

    Includes whether the stage is locked, available, in_progress, or completed.
    """
    try:
        # Get stage
        stage = await service.get_stage_by_id(stage_id)

        # Get user progress for status
        progress = await service.get_progress(user_id)
        stage_data = progress.stage_progress.get(stage_id, {})

        can_access = await service.check_prerequisites(user_id, stage_id)
        status = stage_data.get("status", "locked")
        if can_access and status == "locked":
            status = "available"

        return StageWithStatus(
            id=stage.id,
            number=stage.number,
            name=stage.name,
            slug=stage.slug,
            description=stage.description,
            learning_objectives=stage.learning_objectives,
            estimated_hours=stage.estimated_hours,
            content_count=stage.content_count,
            prerequisite_stage_id=stage.prerequisite_stage_id,
            is_active=stage.is_active,
            status=status,
            percentage_complete=stage_data.get("percentage", 0.0),
            is_accessible=can_access,
        )
    except NotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.to_dict())


@router.get("/stages/{stage_id}/content", response_model=list[ContentItemResponse])
async def get_stage_content(
    stage_id: str,
    service: ServiceDep,
    user_id: CurrentUserDep,
) -> list[ContentItemResponse]:
    """Get content items for a stage.

    Requires prerequisite completion to access (FR-001).
    """
    try:
        # Verify access
        await service.verify_stage_access(user_id, stage_id)

        # Get stage with content
        stage = await service.get_stage_with_content(stage_id)

        # Get user's completions for this stage
        progress = await service.get_progress(user_id)
        completed_ids = {
            c.content_item_id
            for c in progress.content_completions
            if c.content_item.stage_id == stage_id
        }

        return [
            ContentItemResponse(
                id=item.id,
                title=item.title,
                slug=item.slug,
                content_type=item.content_type,
                order=item.order,
                estimated_minutes=item.estimated_minutes,
                is_required=item.is_required,
                is_completed=item.id in completed_ids,
            )
            for item in sorted(stage.content_items, key=lambda x: x.order)
            if item.is_active
        ]
    except PrerequisiteNotMetError as e:
        raise HTTPException(status_code=e.status_code, detail=e.to_dict())
    except NotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.to_dict())


# === Progress Endpoints ===


@router.get("/progress", response_model=ProgressResponse)
async def get_progress(
    service: ServiceDep,
    user_id: CurrentUserDep,
) -> ProgressResponse:
    """Get current user's overall progress."""
    progress = await service.get_progress(user_id)
    return ProgressResponse.model_validate(progress)


@router.get("/progress/path", response_model=LearningPathResponse)
async def get_learning_path(
    service: ServiceDep,
    user_id: CurrentUserDep,
) -> LearningPathResponse:
    """Get learning path visualization (FR-012).

    Returns all stages with their status and the user's current position.
    """
    return await service.get_learning_path(user_id)


@router.post(
    "/progress/content/{content_id}/complete",
    response_model=CompleteContentResponse,
)
async def complete_content(
    content_id: str,
    request: CompleteContentRequest,
    service: ServiceDep,
    user_id: CurrentUserDep,
) -> CompleteContentResponse:
    """Mark a content item as complete.

    Updates user progress and may trigger badge issuance if stage completed.
    """
    try:
        return await service.complete_content(
            user_id=user_id,
            content_id=content_id,
            time_spent_minutes=request.time_spent_minutes,
            score=request.score,
        )
    except PrerequisiteNotMetError as e:
        raise HTTPException(status_code=e.status_code, detail=e.to_dict())
    except NotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.to_dict())


@router.get(
    "/progress/stages/{stage_id}/unlock",
    response_model=dict,
)
async def check_stage_unlock(
    stage_id: str,
    service: ServiceDep,
    user_id: CurrentUserDep,
) -> dict:
    """Check if a stage is unlocked for the user.

    Returns unlock status and requirements if locked.
    """
    try:
        can_access = await service.check_prerequisites(user_id, stage_id)
        stage = await service.get_stage_by_id(stage_id)

        result = {
            "stage_id": stage_id,
            "is_unlocked": can_access,
        }

        if not can_access and stage.prerequisite_stage_id:
            prereq = await service.get_stage_by_id(stage.prerequisite_stage_id)
            progress = await service.get_progress(user_id)
            prereq_data = progress.stage_progress.get(prereq.id, {})

            result["required_stage"] = {
                "id": prereq.id,
                "name": prereq.name,
                "current_percentage": prereq_data.get("percentage", 0),
            }

        return result
    except NotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.to_dict())


# === Badge Endpoints ===


@router.get("/badges", response_model=list[UserBadgeResponse])
async def get_user_badges(
    service: ServiceDep,
    user_id: CurrentUserDep,
) -> list[UserBadgeResponse]:
    """Get all badges earned by the current user."""
    badges = await service.get_user_badges(user_id)
    return [UserBadgeResponse.model_validate(b) for b in badges]


# === Certificate Endpoints ===


@router.get("/certificate", response_model=CertificateResponse | None)
async def get_certificate(
    service: ServiceDep,
    user_id: CurrentUserDep,
) -> CertificateResponse | None:
    """Get user's completion certificate if earned."""
    certificate = await service.get_certificate(user_id)
    if certificate:
        return CertificateResponse.model_validate(certificate)
    return None


@router.post("/certificate/generate", response_model=CertificateResponse)
async def generate_certificate(
    service: ServiceDep,
    user_id: CurrentUserDep,
) -> CertificateResponse:
    """Generate completion certificate (FR-014).

    Only available after completing all 5 stages.
    """
    try:
        certificate = await service.generate_certificate(user_id)
        return CertificateResponse.model_validate(certificate)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": {"code": "INCOMPLETE_COURSE", "message": str(e)}},
        )


# === Time Estimate Endpoints ===


@router.get(
    "/stages/{stage_id}/time-estimate",
    response_model=TimeEstimateResponse,
)
async def get_time_estimate(
    stage_id: str,
    service: ServiceDep,
    user_id: CurrentUserDep,
) -> TimeEstimateResponse:
    """Get estimated time to complete a stage (FR-007)."""
    try:
        return await service.calculate_time_estimate(user_id, stage_id)
    except NotFoundError as e:
        raise HTTPException(status_code=e.status_code, detail=e.to_dict())
