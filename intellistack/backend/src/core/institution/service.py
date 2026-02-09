"""Institution management service with cohort and analytics support."""

from datetime import datetime, timezone
from typing import Optional, List
import re

from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status

from src.core.institution.models import (
    Institution,
    InstitutionMember,
    Cohort,
    CohortEnrollment,
    CohortInstructor,
)
from src.core.analytics.models import CohortAnalytics, InstitutionAnalytics
from src.core.institution.schemas import (
    InstitutionCreate,
    InstitutionUpdate,
    InstitutionResponse,
    CohortCreate,
    CohortUpdate,
    CohortResponse,
    EnrollmentCreate,
    InstitutionAnalyticsResponse,
    CohortAnalyticsResponse,
)
from src.core.institution.webhooks import fire_enrollment_webhook


def generate_slug(name: str) -> str:
    """Generate URL-friendly slug from name."""
    slug = name.lower()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug.strip('-')


async def create_institution(
    db: AsyncSession,
    institution_data: InstitutionCreate,
    creator_id: str,
) -> InstitutionResponse:
    """
    Create new institution.

    Args:
        db: Database session
        institution_data: Institution data
        creator_id: Creator user ID

    Returns:
        InstitutionResponse: Created institution
    """
    # Generate unique slug
    base_slug = generate_slug(institution_data.name)
    slug = base_slug
    counter = 1

    while True:
        result = await db.execute(select(Institution).where(Institution.slug == slug))
        if not result.scalar_one_or_none():
            break
        slug = f"{base_slug}-{counter}"
        counter += 1

    # Create institution
    institution = Institution(
        name=institution_data.name,
        slug=slug,
        institution_type=institution_data.institution_type,
        domain=institution_data.domain,
        logo_url=str(institution_data.logo_url) if institution_data.logo_url else None,
        primary_color=institution_data.primary_color,
        secondary_color=institution_data.secondary_color,
        welcome_message=institution_data.welcome_message,
        webhook_url=str(institution_data.webhook_url) if institution_data.webhook_url else None,
        simulation_quota_hours=institution_data.simulation_quota_hours,
    )

    db.add(institution)
    await db.flush()

    # Add creator as admin
    member = InstitutionMember(
        institution_id=institution.id,
        user_id=creator_id,
        role="admin",
    )
    db.add(member)

    # Initialize analytics
    analytics = InstitutionAnalytics(institution_id=institution.id)
    db.add(analytics)

    await db.commit()
    await db.refresh(institution)

    return InstitutionResponse.model_validate(institution)


async def update_institution(
    db: AsyncSession,
    institution_id: str,
    update_data: InstitutionUpdate,
) -> InstitutionResponse:
    """
    Update institution settings.

    Args:
        db: Database session
        institution_id: Institution ID
        update_data: Update data

    Returns:
        InstitutionResponse: Updated institution
    """
    result = await db.execute(select(Institution).where(Institution.id == institution_id))
    institution = result.scalar_one_or_none()

    if not institution:
        raise HTTPException(status_code=404, detail="Institution not found")

    # Update fields
    if update_data.name:
        institution.name = update_data.name
    if update_data.logo_url is not None:
        institution.logo_url = str(update_data.logo_url) if update_data.logo_url else None
    if update_data.primary_color:
        institution.primary_color = update_data.primary_color
    if update_data.secondary_color is not None:
        institution.secondary_color = update_data.secondary_color
    if update_data.welcome_message is not None:
        institution.welcome_message = update_data.welcome_message
    if update_data.webhook_url is not None:
        institution.webhook_url = str(update_data.webhook_url) if update_data.webhook_url else None
    if update_data.custom_css is not None:
        institution.custom_css = update_data.custom_css
    if update_data.settings is not None:
        institution.settings = update_data.settings

    await db.commit()
    await db.refresh(institution)

    return InstitutionResponse.model_validate(institution)


async def create_cohort(
    db: AsyncSession,
    cohort_data: CohortCreate,
    creator_id: str,
) -> CohortResponse:
    """
    Create new cohort.

    Args:
        db: Database session
        cohort_data: Cohort data
        creator_id: Creator user ID

    Returns:
        CohortResponse: Created cohort
    """
    # Verify institution exists
    result = await db.execute(
        select(Institution).where(Institution.id == cohort_data.institution_id)
    )
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Institution not found")

    # Create cohort
    cohort = Cohort(
        institution_id=cohort_data.institution_id,
        name=cohort_data.name,
        description=cohort_data.description,
        start_date=cohort_data.start_date,
        end_date=cohort_data.end_date,
        enrollment_limit=cohort_data.enrollment_limit,
        is_enrollment_open=cohort_data.is_enrollment_open,
        created_by=creator_id,
    )

    db.add(cohort)
    await db.flush()

    # Initialize analytics
    analytics = CohortAnalytics(cohort_id=cohort.id)
    db.add(analytics)

    await db.commit()
    await db.refresh(cohort)

    response = CohortResponse.model_validate(cohort)
    response.enrolled_count = 0

    return response


async def enroll_student(
    db: AsyncSession,
    cohort_id: str,
    user_id: str,
    enrolled_by: str,
) -> None:
    """
    Enroll student in cohort.

    Args:
        db: Database session
        cohort_id: Cohort ID
        user_id: Student user ID
        enrolled_by: Admin who is enrolling

    Raises:
        HTTPException: If cohort full, closed, or student already enrolled
    """
    # Get cohort
    result = await db.execute(
        select(Cohort)
        .options(selectinload(Cohort.enrollments))
        .where(Cohort.id == cohort_id)
    )
    cohort = result.scalar_one_or_none()

    if not cohort:
        raise HTTPException(status_code=404, detail="Cohort not found")

    # Check enrollment status
    if not cohort.is_enrollment_open:
        raise HTTPException(status_code=400, detail="Enrollment is closed for this cohort")

    # Check enrollment limit
    if cohort.enrollment_limit:
        current_count = len([e for e in cohort.enrollments if e.dropped_at is None])
        if current_count >= cohort.enrollment_limit:
            raise HTTPException(status_code=400, detail="Cohort is full")

    # Check if already enrolled
    existing = await db.execute(
        select(CohortEnrollment).where(
            and_(
                CohortEnrollment.cohort_id == cohort_id,
                CohortEnrollment.user_id == user_id,
                CohortEnrollment.dropped_at.is_(None),
            )
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Student already enrolled in this cohort")

    # Create enrollment
    enrollment = CohortEnrollment(
        cohort_id=cohort_id,
        user_id=user_id,
        enrolled_by=enrolled_by,
    )
    db.add(enrollment)
    await db.commit()
    await db.refresh(enrollment)

    # Fire webhook event (FR-039)
    await fire_enrollment_webhook(
        db,
        cohort.institution_id,
        cohort_id,
        user_id,
        enrollment.enrolled_at,
    )

    # TODO: Send notification to student


async def assign_instructor(
    db: AsyncSession,
    cohort_id: str,
    instructor_id: str,
    assigned_by: str,
) -> None:
    """
    Assign instructor to cohort.

    Args:
        db: Database session
        cohort_id: Cohort ID
        instructor_id: Instructor user ID
        assigned_by: Admin who is assigning

    Raises:
        HTTPException: If cohort not found or instructor already assigned
    """
    # Verify cohort exists
    result = await db.execute(select(Cohort).where(Cohort.id == cohort_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Cohort not found")

    # Check if already assigned
    existing = await db.execute(
        select(CohortInstructor).where(
            and_(
                CohortInstructor.cohort_id == cohort_id,
                CohortInstructor.user_id == instructor_id,
            )
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Instructor already assigned to this cohort")

    # Create assignment
    assignment = CohortInstructor(
        cohort_id=cohort_id,
        user_id=instructor_id,
        assigned_by=assigned_by,
    )
    db.add(assignment)
    await db.commit()


async def get_cohort_analytics(
    db: AsyncSession,
    cohort_id: str,
) -> CohortAnalyticsResponse:
    """
    Get analytics for cohort.

    Args:
        db: Database session
        cohort_id: Cohort ID

    Returns:
        CohortAnalyticsResponse: Analytics data

    Raises:
        HTTPException: If cohort not found
    """
    result = await db.execute(
        select(CohortAnalytics).where(CohortAnalytics.cohort_id == cohort_id)
    )
    analytics = result.scalar_one_or_none()

    if not analytics:
        raise HTTPException(status_code=404, detail="Cohort analytics not found")

    return CohortAnalyticsResponse.model_validate(analytics)


async def get_institution_analytics(
    db: AsyncSession,
    institution_id: str,
) -> InstitutionAnalyticsResponse:
    """
    Get analytics for institution.

    Args:
        db: Database session
        institution_id: Institution ID

    Returns:
        InstitutionAnalyticsResponse: Analytics data

    Raises:
        HTTPException: If institution not found
    """
    result = await db.execute(
        select(InstitutionAnalytics).where(
            InstitutionAnalytics.institution_id == institution_id
        )
    )
    analytics = result.scalar_one_or_none()

    if not analytics:
        raise HTTPException(status_code=404, detail="Institution analytics not found")

    return InstitutionAnalyticsResponse.model_validate(analytics)


async def refresh_cohort_analytics(
    db: AsyncSession,
    cohort_id: str,
) -> None:
    """
    Recalculate cohort analytics from raw data.

    Args:
        db: Database session
        cohort_id: Cohort ID
    """
    # Get or create analytics
    result = await db.execute(
        select(CohortAnalytics).where(CohortAnalytics.cohort_id == cohort_id)
    )
    analytics = result.scalar_one_or_none()

    if not analytics:
        analytics = CohortAnalytics(cohort_id=cohort_id)
        db.add(analytics)

    # Count enrollments
    enrollment_result = await db.execute(
        select(func.count()).where(
            and_(
                CohortEnrollment.cohort_id == cohort_id,
                CohortEnrollment.dropped_at.is_(None),
            )
        )
    )
    analytics.total_students = enrollment_result.scalar() or 0

    # TODO: Calculate other metrics from Progress, UserBadge, etc.
    # For now, just update timestamp
    analytics.last_updated = datetime.now(timezone.utc)

    await db.commit()
