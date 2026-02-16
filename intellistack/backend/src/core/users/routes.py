"""User API routes for profile and onboarding."""

import logging
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.database import get_session as get_db
from src.core.auth.dependencies import get_current_user, AuthenticatedUser
from src.core.auth.models import User
from src.core.learning.models import Progress, Stage
from sqlalchemy import select
from .schemas import OnboardingData, UserPreferences, UserProfileResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/users", tags=["users"])


async def get_or_create_user(
    user: AuthenticatedUser, db: AsyncSession
) -> User:
    """
    JIT provisioning: Get existing user or create from JWT claims.

    This enables seamless signup - when a user authenticates via Better-Auth,
    they are automatically created in the backend's users table.
    """
    stmt = select(User).where(User.id == user.id)
    result = await db.execute(stmt)
    db_user = result.scalar_one_or_none()

    if not db_user:
        # Create user from JWT claims
        # password_hash is set to a placeholder — auth is handled by Better-Auth,
        # the backend never verifies passwords directly.
        db_user = User(
            id=user.id,
            email=user.email,
            name=user.name or user.email.split("@")[0],
            password_hash="!better-auth-managed",
            role=user.role,
            email_verified=user.email_verified,
            is_active=True,
            current_stage=1,
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        logger.info(f"JIT provisioned user: {user.email} (id={user.id})")

    return db_user


@router.get("/me", response_model=UserProfileResponse)
async def get_current_user_profile(
    user: AuthenticatedUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Get the current user's profile.

    Returns user info including preferences and current stage.
    JIT provisions user if not found (signup flow).
    """
    # JIT provisioning: create user if doesn't exist
    db_user = await get_or_create_user(user, db)

    # Parse preferences from JSON
    preferences = None
    if db_user.preferences:
        try:
            preferences = UserPreferences(**db_user.preferences)
        except Exception:
            preferences = UserPreferences()

    return UserProfileResponse(
        id=db_user.id,
        email=db_user.email,
        name=db_user.name,
        role=db_user.role or "student",
        email_verified=db_user.email_verified or False,
        preferences=preferences,
        current_stage=db_user.current_stage or 1,
    )


@router.post("/onboarding")
async def save_onboarding_data(
    data: OnboardingData,
    user: AuthenticatedUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Save onboarding preferences.

    Called after completing the onboarding wizard.
    JIT provisions user if not found.
    """
    # JIT provisioning: create user if doesn't exist
    db_user = await get_or_create_user(user, db)

    # Build preferences object
    preferences = {
        "system": data.system_preferences.model_dump(),
        "learning": data.learning_preferences.model_dump(),
        "background": data.background_level.model_dump(),
        "onboarding_completed": True,
        "onboarding_completed_at": datetime.utcnow().isoformat(),
    }

    # Determine recommended starting stage based on background
    starting_stage = 1
    bg = data.background_level

    # If user has intermediate+ programming AND some robotics/linux experience, start at stage 2
    if (
        bg.programming_experience in ("intermediate", "advanced")
        and bg.robotics_experience in ("hobbyist", "academic", "professional")
        and bg.linux_familiarity in ("comfortable", "expert")
    ):
        starting_stage = 2

    # Update user in database
    stmt = (
        update(User)
        .where(User.id == user.id)
        .values(
            preferences=preferences,
            current_stage=starting_stage,
            onboarding_completed=True,
        )
    )
    await db.execute(stmt)
    await db.commit()

    logger.info(f"Saved onboarding for user {user.id}, starting stage: {starting_stage}")

    return {
        "success": True,
        "recommended_stage": starting_stage,
        "message": f"Onboarding complete! Starting at Stage {starting_stage}",
    }


@router.patch("/preferences")
async def update_preferences(
    preferences: dict,
    user: AuthenticatedUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Update user preferences.

    Merges provided preferences with existing ones.
    JIT provisions user if not found.
    """
    # JIT provisioning: create user if doesn't exist
    db_user = await get_or_create_user(user, db)

    # Merge preferences
    current_prefs = db_user.preferences or {}
    updated_prefs = {**current_prefs, **preferences}

    # Update
    stmt = (
        update(User)
        .where(User.id == user.id)
        .values(preferences=updated_prefs)
    )
    await db.execute(stmt)
    await db.commit()

    return {"success": True, "preferences": updated_prefs}


@router.get("/stage")
async def get_current_stage(
    user: AuthenticatedUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Get user's current learning stage.

    Returns the stage number (1-5) the user has unlocked.
    JIT provisions user if not found.
    """
    # JIT provisioning: create user if doesn't exist
    db_user = await get_or_create_user(user, db)

    # Get user's progress to determine actual current stage
    result = await db.execute(
        select(Progress).where(Progress.user_id == user.id)
    )
    progress = result.scalar_one_or_none()

    if progress and progress.current_stage_id:
        # Get the stage number from the current stage ID
        stage_result = await db.execute(
            select(Stage.number).where(Stage.id == progress.current_stage_id)
        )
        stage_number = stage_result.scalar_one_or_none()
        if stage_number is not None:
            return {"stage": stage_number}

    # Fallback to user's current_stage field or default to 1
    return {"stage": db_user.current_stage or 1}
