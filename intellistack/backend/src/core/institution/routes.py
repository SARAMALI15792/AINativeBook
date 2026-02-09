"""Institution management API routes."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth.models import User
from src.core.auth.routes import get_current_active_user
from src.core.institution import service
from src.core.institution.schemas import (
    InstitutionCreate,
    InstitutionUpdate,
    InstitutionResponse,
    CohortCreate,
    CohortUpdate,
    CohortResponse,
    EnrollmentCreate,
    InstructorAssignment,
    CohortAnalyticsResponse,
    InstitutionAnalyticsResponse,
)
from src.shared.database import get_session

router = APIRouter(prefix="/institutions", tags=["institutions"])


@router.post("/", response_model=InstitutionResponse, status_code=status.HTTP_201_CREATED)
async def create_institution(
    institution_data: InstitutionCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
):
    """
    Create new institution (platform admin only).

    Args:
        institution_data: Institution data
        current_user: Current user (must be platform admin)
        db: Database session

    Returns:
        InstitutionResponse: Created institution
    """
    # TODO: Check platform_admin role
    return await service.create_institution(db, institution_data, str(current_user.id))


@router.put("/{institution_id}", response_model=InstitutionResponse)
async def update_institution(
    institution_id: str,
    update_data: InstitutionUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
):
    """
    Update institution settings (institution admin only).

    Args:
        institution_id: Institution ID
        update_data: Update data
        current_user: Current user (must be institution admin)
        db: Database session

    Returns:
        InstitutionResponse: Updated institution
    """
    # TODO: Check institution_admin role for this institution
    return await service.update_institution(db, institution_id, update_data)


@router.post("/cohorts", response_model=CohortResponse, status_code=status.HTTP_201_CREATED)
async def create_cohort(
    cohort_data: CohortCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
):
    """
    Create new cohort (institution admin only).

    Args:
        cohort_data: Cohort data
        current_user: Current user
        db: Database session

    Returns:
        CohortResponse: Created cohort
    """
    return await service.create_cohort(db, cohort_data, str(current_user.id))


@router.post("/cohorts/{cohort_id}/enroll", status_code=status.HTTP_204_NO_CONTENT)
async def enroll_student_in_cohort(
    cohort_id: str,
    enrollment: EnrollmentCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
):
    """
    Enroll student in cohort (admin/instructor only).

    Args:
        cohort_id: Cohort ID
        enrollment: Enrollment data
        current_user: Current user
        db: Database session
    """
    await service.enroll_student(
        db,
        cohort_id,
        enrollment.user_id,
        str(current_user.id),
    )


@router.post("/cohorts/{cohort_id}/instructors", status_code=status.HTTP_204_NO_CONTENT)
async def assign_instructor_to_cohort(
    cohort_id: str,
    assignment: InstructorAssignment,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
):
    """
    Assign instructor to cohort (admin only).

    Args:
        cohort_id: Cohort ID
        assignment: Instructor assignment
        current_user: Current user
        db: Database session
    """
    await service.assign_instructor(
        db,
        cohort_id,
        assignment.user_id,
        str(current_user.id),
    )


@router.get("/cohorts/{cohort_id}/analytics", response_model=CohortAnalyticsResponse)
async def get_cohort_analytics(
    cohort_id: str,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
):
    """
    Get cohort analytics (admin/instructor only).

    Args:
        cohort_id: Cohort ID
        current_user: Current user
        db: Database session

    Returns:
        CohortAnalyticsResponse: Analytics data
    """
    return await service.get_cohort_analytics(db, cohort_id)


@router.get("/{institution_id}/analytics", response_model=InstitutionAnalyticsResponse)
async def get_institution_analytics(
    institution_id: str,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
):
    """
    Get institution-wide analytics (institution admin only).

    Args:
        institution_id: Institution ID
        current_user: Current user
        db: Database session

    Returns:
        InstitutionAnalyticsResponse: Analytics data
    """
    return await service.get_institution_analytics(db, institution_id)


@router.post("/cohorts/{cohort_id}/analytics/refresh", status_code=status.HTTP_204_NO_CONTENT)
async def refresh_analytics(
    cohort_id: str,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
):
    """
    Refresh cohort analytics (recalculate from raw data).

    Args:
        cohort_id: Cohort ID
        current_user: Current user
        db: Database session
    """
    await service.refresh_cohort_analytics(db, cohort_id)
