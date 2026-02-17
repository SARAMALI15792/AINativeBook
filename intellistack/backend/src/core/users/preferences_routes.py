"""
User Preferences API Routes
Handles onboarding flow and preference management
Sprint 3: Personalization Engine
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, Field
import structlog

from src.shared.database import get_db
from src.core.auth.dependencies import get_current_user
from src.core.auth.models import User
from src.ai.personalization.models import (
    PersonalizationProfile,
    LearningStyle,
    LearningPace,
)

logger = structlog.get_logger()

router = APIRouter(prefix="/api/v1/users/preferences", tags=["User Preferences"])


# Pydantic schemas for request/response
class OnboardingPreferencesRequest(BaseModel):
    """User preferences collected during onboarding"""

    # System setup
    operating_system: Optional[str] = Field(None, description="Linux/Mac/Windows")
    preferred_ide: Optional[str] = Field(None, description="VSCode/PyCharm/Vim")
    shell: Optional[str] = Field(None, description="bash/zsh/fish")

    # Learning style
    learning_style: LearningStyle = Field(..., description="visual/auditory/kinesthetic/reading")
    learning_pace: LearningPace = Field(LearningPace.MODERATE, description="slow/moderate/fast")
    goal_timeframe: Optional[str] = Field(None, description="3/6/12 months")

    # Background
    programming_experience: Optional[str] = Field(None, description="none/beginner/intermediate/advanced")
    robotics_experience: Optional[str] = Field(None, description="none/hobbyist/professional")
    math_background: Optional[str] = Field(None, description="basic/calculus/linear_algebra")
    linux_familiarity: Optional[str] = Field(None, description="none/basic/advanced")

    # Interests
    focus_areas: Optional[list[str]] = Field(default_factory=list, description="manipulation/navigation/vision/AI")
    domain_preference: Optional[str] = Field(None, description="healthcare/manufacturing/service/research")
    preferred_language: str = Field("en", description="en/ur")

    # Adaptation settings
    adaptive_complexity: bool = Field(True, description="Enable adaptive content complexity")
    personalized_exercises: bool = Field(True, description="Generate personalized exercises")
    personalized_time_estimates: bool = Field(True, description="Show personalized time estimates")


class PreferencesResponse(BaseModel):
    """User preferences response"""

    id: str
    user_id: str

    # Background
    educational_background: Optional[str]
    prior_experience: Optional[str]
    technical_skills: Optional[list[str]]
    learning_goals: Optional[str]

    # Learning preferences
    learning_style: Optional[str]
    learning_pace: str
    preferred_language: str

    # Domain preferences
    preferred_examples_domain: Optional[str]
    interest_areas: Optional[list[str]]

    # Adaptation settings
    adaptive_complexity: bool
    personalized_exercises: bool
    personalized_time_estimates: bool

    # Privacy
    share_progress_with_instructors: bool
    share_with_peers: bool
    allow_ai_personalization: bool


@router.post("/onboarding", response_model=PreferencesResponse)
async def complete_onboarding(
    preferences: OnboardingPreferencesRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Complete onboarding flow by saving user preferences
    This is called after user registration to collect learning preferences
    """
    try:
        # Check if profile already exists
        result = await db.execute(
            select(PersonalizationProfile).where(
                PersonalizationProfile.user_id == str(current_user.id)
            )
        )
        profile = result.scalar_one_or_none()

        if profile:
            # Update existing profile
            profile.learning_style = preferences.learning_style
            profile.learning_pace = preferences.learning_pace
            profile.preferred_language = preferences.preferred_language
            profile.preferred_examples_domain = preferences.domain_preference
            profile.interest_areas = preferences.focus_areas
            profile.adaptive_complexity = preferences.adaptive_complexity
            profile.personalized_exercises = preferences.personalized_exercises
            profile.personalized_time_estimates = preferences.personalized_time_estimates

            # Build background description
            background_parts = []
            if preferences.programming_experience:
                background_parts.append(f"Programming: {preferences.programming_experience}")
            if preferences.robotics_experience:
                background_parts.append(f"Robotics: {preferences.robotics_experience}")
            if preferences.math_background:
                background_parts.append(f"Math: {preferences.math_background}")
            if preferences.linux_familiarity:
                background_parts.append(f"Linux: {preferences.linux_familiarity}")

            profile.prior_experience = ", ".join(background_parts)

            # Build technical skills
            skills = []
            if preferences.operating_system:
                skills.append(preferences.operating_system)
            if preferences.preferred_ide:
                skills.append(preferences.preferred_ide)
            if preferences.shell:
                skills.append(preferences.shell)
            profile.technical_skills = skills

            # Set learning goals
            if preferences.goal_timeframe:
                profile.learning_goals = f"Complete Physical AI course in {preferences.goal_timeframe}"

        else:
            # Create new profile
            profile = PersonalizationProfile(
                user_id=str(current_user.id),
                learning_style=preferences.learning_style,
                learning_pace=preferences.learning_pace,
                preferred_language=preferences.preferred_language,
                preferred_examples_domain=preferences.domain_preference,
                interest_areas=preferences.focus_areas,
                adaptive_complexity=preferences.adaptive_complexity,
                personalized_exercises=preferences.personalized_exercises,
                personalized_time_estimates=preferences.personalized_time_estimates,
                prior_experience=", ".join([
                    f"Programming: {preferences.programming_experience or 'none'}",
                    f"Robotics: {preferences.robotics_experience or 'none'}",
                    f"Math: {preferences.math_background or 'basic'}",
                    f"Linux: {preferences.linux_familiarity or 'none'}",
                ]),
                technical_skills=[
                    preferences.operating_system,
                    preferences.preferred_ide,
                    preferences.shell,
                ] if preferences.operating_system else [],
                learning_goals=f"Complete Physical AI course in {preferences.goal_timeframe}" if preferences.goal_timeframe else None,
            )
            db.add(profile)

        await db.commit()
        await db.refresh(profile)

        logger.info(
            "onboarding_completed",
            user_id=str(current_user.id),
            learning_style=preferences.learning_style,
            language=preferences.preferred_language,
        )

        return PreferencesResponse(
            id=str(profile.id),
            user_id=str(profile.user_id),
            educational_background=profile.educational_background,
            prior_experience=profile.prior_experience,
            technical_skills=profile.technical_skills or [],
            learning_goals=profile.learning_goals,
            learning_style=profile.learning_style.value if profile.learning_style else None,
            learning_pace=profile.learning_pace.value,
            preferred_language=profile.preferred_language,
            preferred_examples_domain=profile.preferred_examples_domain,
            interest_areas=profile.interest_areas or [],
            adaptive_complexity=profile.adaptive_complexity,
            personalized_exercises=profile.personalized_exercises,
            personalized_time_estimates=profile.personalized_time_estimates,
            share_progress_with_instructors=profile.share_progress_with_instructors,
            share_with_peers=profile.share_with_peers,
            allow_ai_personalization=profile.allow_ai_personalization,
        )

    except Exception as e:
        logger.error("onboarding_error", error=str(e), user_id=str(current_user.id))
        await db.rollback()
        raise HTTPException(status_code=500, detail="Failed to save preferences")


@router.get("", response_model=PreferencesResponse)
async def get_preferences(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get current user's preferences"""
    try:
        result = await db.execute(
            select(PersonalizationProfile).where(
                PersonalizationProfile.user_id == str(current_user.id)
            )
        )
        profile = result.scalar_one_or_none()

        if not profile:
            raise HTTPException(
                status_code=404,
                detail="Preferences not found. Complete onboarding first.",
            )

        return PreferencesResponse(
            id=str(profile.id),
            user_id=str(profile.user_id),
            educational_background=profile.educational_background,
            prior_experience=profile.prior_experience,
            technical_skills=profile.technical_skills or [],
            learning_goals=profile.learning_goals,
            learning_style=profile.learning_style.value if profile.learning_style else None,
            learning_pace=profile.learning_pace.value,
            preferred_language=profile.preferred_language,
            preferred_examples_domain=profile.preferred_examples_domain,
            interest_areas=profile.interest_areas or [],
            adaptive_complexity=profile.adaptive_complexity,
            personalized_exercises=profile.personalized_exercises,
            personalized_time_estimates=profile.personalized_time_estimates,
            share_progress_with_instructors=profile.share_progress_with_instructors,
            share_with_peers=profile.share_with_peers,
            allow_ai_personalization=profile.allow_ai_personalization,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("get_preferences_error", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to retrieve preferences")


@router.put("", response_model=PreferencesResponse)
async def update_preferences(
    preferences: OnboardingPreferencesRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update user preferences"""
    # Reuse onboarding logic (it handles both create and update)
    return await complete_onboarding(preferences, current_user, db)


@router.post("/reset")
async def reset_preferences(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Reset preferences to defaults"""
    try:
        result = await db.execute(
            select(PersonalizationProfile).where(
                PersonalizationProfile.user_id == str(current_user.id)
            )
        )
        profile = result.scalar_one_or_none()

        if not profile:
            raise HTTPException(status_code=404, detail="Preferences not found")

        # Reset to defaults
        profile.learning_style = None
        profile.learning_pace = LearningPace.MODERATE
        profile.preferred_language = "en"
        profile.preferred_examples_domain = None
        profile.interest_areas = []
        profile.adaptive_complexity = True
        profile.personalized_exercises = True
        profile.personalized_time_estimates = True
        profile.last_reset_at = func.now()

        await db.commit()

        logger.info("preferences_reset", user_id=str(current_user.id))

        return {"message": "Preferences reset to defaults"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error("reset_preferences_error", error=str(e))
        await db.rollback()
        raise HTTPException(status_code=500, detail="Failed to reset preferences")


@router.post("/language")
async def update_language(
    language: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Update preferred language
    Quick endpoint for language toggle
    """
    if language not in ["en", "ur"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid language. Supported: en, ur",
        )

    try:
        result = await db.execute(
            select(PersonalizationProfile).where(
                PersonalizationProfile.user_id == str(current_user.id)
            )
        )
        profile = result.scalar_one_or_none()

        if not profile:
            # Create minimal profile with just language
            profile = PersonalizationProfile(
                user_id=str(current_user.id),
                preferred_language=language,
            )
            db.add(profile)
        else:
            profile.preferred_language = language

        await db.commit()

        logger.info(
            "language_updated",
            user_id=str(current_user.id),
            language=language,
        )

        return {
            "message": f"Language updated to {language}",
            "language": language,
        }

    except Exception as e:
        logger.error("update_language_error", error=str(e))
        await db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update language")
