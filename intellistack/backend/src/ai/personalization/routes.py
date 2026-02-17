"""
Personalization Routes
API endpoints for personalized content delivery and variant management
Sprint 3: Personalization Engine
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
import structlog

from src.shared.database import get_db
from src.core.auth.dependencies import get_current_user
from src.core.auth.models import User
from src.core.content.models import Content
from src.core.content.enhanced_models import ContentVariant, ComplexityLevel
from src.ai.personalization.service import PersonalizationService
from src.ai.personalization.models import PersonalizationProfile, ChapterPersonalization
from src.ai.shared.llm_client import LLMClient

logger = structlog.get_logger()

router = APIRouter(prefix="/api/v1/personalization", tags=["Personalization"])

# Initialize services
llm_client = LLMClient()
personalization_service = PersonalizationService(llm_client)


class PersonalizedExamplesRequest(BaseModel):
    """Request to generate personalized examples"""
    content_id: str
    domain: Optional[str] = None  # Override profile domain


class PersonalizedExamplesResponse(BaseModel):
    """Personalized examples response"""
    content_id: str
    domain: str
    examples: list[dict]


class ComplexityAdjustmentRequest(BaseModel):
    """Request to adjust content complexity"""
    content_id: str
    target_complexity: str  # beginner/intermediate/advanced


class TimeEstimateResponse(BaseModel):
    """Personalized time estimate response"""
    content_id: str
    base_time_minutes: int
    personalized_time_minutes: int
    multiplier: float
    factors: dict


@router.get("/content/{content_id}/variant")
async def get_personalized_variant(
    content_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Get personalized content variant for user
    Returns appropriate variant based on user profile
    """
    try:
        # Get personalized variant
        variant = await personalization_service.get_personalized_content(
            content_id=content_id,
            user_id=str(current_user.id),
            db=db,
        )

        if not variant:
            raise HTTPException(
                status_code=404,
                detail="No suitable variant found for this content",
            )

        logger.info(
            "personalized_variant_served",
            content_id=content_id,
            user_id=str(current_user.id),
            variant_type=variant.variant_type,
            complexity=variant.complexity_level,
            language=variant.language_code,
        )

        return {
            "variant_id": variant.id,
            "content_id": variant.content_id,
            "variant_type": variant.variant_type,
            "language_code": variant.language_code,
            "complexity_level": variant.complexity_level,
            "content_json": variant.content_json,
            "word_count": variant.word_count,
            "estimated_reading_time": variant.estimated_reading_time,
            "personalized": True,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error("get_variant_error", error=str(e), content_id=content_id)
        raise HTTPException(status_code=500, detail="Failed to get personalized variant")


@router.post("/content/{content_id}/examples", response_model=PersonalizedExamplesResponse)
async def generate_personalized_examples(
    content_id: str,
    request: Optional[PersonalizedExamplesRequest] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Generate domain-specific examples for content
    E.g., convert generic robot examples to medical robot examples
    """
    try:
        # Get content
        content_result = await db.execute(
            select(Content).where(Content.id == content_id)
        )
        content = content_result.scalar_one_or_none()

        if not content:
            raise HTTPException(status_code=404, detail="Content not found")

        # Get user profile
        profile_result = await db.execute(
            select(PersonalizationProfile).where(
                PersonalizationProfile.user_id == str(current_user.id)
            )
        )
        profile = profile_result.scalar_one_or_none()

        if not profile:
            raise HTTPException(
                status_code=404,
                detail="User profile not found. Complete onboarding first.",
            )

        # Use domain from request or profile
        domain = request.domain if request and request.domain else profile.preferred_examples_domain

        if not domain:
            raise HTTPException(
                status_code=400,
                detail="No domain specified. Set domain preference in profile.",
            )

        # Generate examples
        examples = await personalization_service.generate_personalized_examples(
            content=content,
            profile=profile,
        )

        logger.info(
            "personalized_examples_generated",
            content_id=content_id,
            domain=domain,
            count=len(examples),
            user_id=str(current_user.id),
        )

        return PersonalizedExamplesResponse(
            content_id=content_id,
            domain=domain,
            examples=examples,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("generate_examples_error", error=str(e), content_id=content_id)
        raise HTTPException(status_code=500, detail="Failed to generate examples")


@router.post("/content/{content_id}/adjust-complexity")
async def adjust_content_complexity(
    content_id: str,
    request: ComplexityAdjustmentRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Adjust content complexity level
    Triggers generation of simplified or advanced variant
    """
    if request.target_complexity not in ["beginner", "intermediate", "advanced"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid complexity level. Use: beginner, intermediate, advanced",
        )

    try:
        # Get content
        content_result = await db.execute(
            select(Content).where(Content.id == content_id)
        )
        content = content_result.scalar_one_or_none()

        if not content:
            raise HTTPException(status_code=404, detail="Content not found")

        # Check if variant already exists
        variant_result = await db.execute(
            select(ContentVariant).where(
                ContentVariant.content_id == content_id,
                ContentVariant.complexity_level == ComplexityLevel(request.target_complexity),
            )
        )
        existing_variant = variant_result.scalar_one_or_none()

        if existing_variant:
            return {
                "message": "Variant already exists",
                "variant_id": existing_variant.id,
                "complexity_level": existing_variant.complexity_level,
            }

        # Trigger complexity adjustment
        variant = await personalization_service.adjust_complexity(
            content=content,
            complexity_level=request.target_complexity,
        )

        if variant:
            logger.info(
                "complexity_adjusted",
                content_id=content_id,
                target_complexity=request.target_complexity,
                user_id=str(current_user.id),
            )

            return {
                "message": "Complexity adjustment complete",
                "variant_id": variant.id,
                "complexity_level": variant.complexity_level,
            }
        else:
            # Variant generation needed (async process)
            logger.info(
                "complexity_adjustment_queued",
                content_id=content_id,
                target_complexity=request.target_complexity,
            )

            return {
                "message": "Complexity adjustment queued",
                "status": "processing",
                "target_complexity": request.target_complexity,
            }

    except HTTPException:
        raise
    except Exception as e:
        logger.error("adjust_complexity_error", error=str(e), content_id=content_id)
        raise HTTPException(status_code=500, detail="Failed to adjust complexity")


@router.get("/content/{content_id}/time-estimate", response_model=TimeEstimateResponse)
async def get_personalized_time_estimate(
    content_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Get personalized time estimate for content
    Adjusts based on user's pace and background
    """
    try:
        # Get content
        content_result = await db.execute(
            select(Content).where(Content.id == content_id)
        )
        content = content_result.scalar_one_or_none()

        if not content:
            raise HTTPException(status_code=404, detail="Content not found")

        # Get user profile
        profile_result = await db.execute(
            select(PersonalizationProfile).where(
                PersonalizationProfile.user_id == str(current_user.id)
            )
        )
        profile = profile_result.scalar_one_or_none()

        if not profile:
            # Return base estimate if no profile
            base_time = content.estimated_reading_time or 30
            return TimeEstimateResponse(
                content_id=content_id,
                base_time_minutes=base_time,
                personalized_time_minutes=base_time,
                multiplier=1.0,
                factors={"note": "No personalization profile found"},
            )

        # Get personalized estimate
        personalized_time = await personalization_service.estimate_personalized_time(
            content=content,
            profile=profile,
        )

        base_time = content.estimated_reading_time or 30
        multiplier = personalized_time / base_time if base_time > 0 else 1.0

        # Build factors explanation
        factors = {
            "learning_pace": profile.learning_pace.value,
            "has_experience": bool(profile.prior_experience),
        }

        logger.info(
            "time_estimate_calculated",
            content_id=content_id,
            base_time=base_time,
            personalized_time=personalized_time,
            multiplier=multiplier,
        )

        return TimeEstimateResponse(
            content_id=content_id,
            base_time_minutes=base_time,
            personalized_time_minutes=personalized_time,
            multiplier=round(multiplier, 2),
            factors=factors,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("time_estimate_error", error=str(e), content_id=content_id)
        raise HTTPException(status_code=500, detail="Failed to calculate time estimate")


@router.post("/content/{content_id}/toggle")
async def toggle_chapter_personalization(
    content_id: str,
    enabled: bool = Query(..., description="Enable or disable personalization"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Toggle personalization for specific chapter
    Allows users to disable personalization per-content
    """
    try:
        # Get user profile
        profile_result = await db.execute(
            select(PersonalizationProfile).where(
                PersonalizationProfile.user_id == str(current_user.id)
            )
        )
        profile = profile_result.scalar_one_or_none()

        if not profile:
            raise HTTPException(
                status_code=404,
                detail="User profile not found. Complete onboarding first.",
            )

        # Get or create chapter personalization
        chapter_result = await db.execute(
            select(ChapterPersonalization).where(
                ChapterPersonalization.profile_id == profile.id,
                ChapterPersonalization.content_id == content_id,
            )
        )
        chapter_pref = chapter_result.scalar_one_or_none()

        if chapter_pref:
            chapter_pref.is_enabled = enabled
        else:
            chapter_pref = ChapterPersonalization(
                profile_id=profile.id,
                content_id=content_id,
                is_enabled=enabled,
            )
            db.add(chapter_pref)

        await db.commit()

        logger.info(
            "chapter_personalization_toggled",
            content_id=content_id,
            enabled=enabled,
            user_id=str(current_user.id),
        )

        return {
            "message": f"Personalization {'enabled' if enabled else 'disabled'} for this chapter",
            "content_id": content_id,
            "enabled": enabled,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error("toggle_personalization_error", error=str(e), content_id=content_id)
        await db.rollback()
        raise HTTPException(status_code=500, detail="Failed to toggle personalization")


@router.get("/stats")
async def get_personalization_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Get personalization statistics for current user
    Shows how content is being adapted
    """
    try:
        # Get user profile
        profile_result = await db.execute(
            select(PersonalizationProfile).where(
                PersonalizationProfile.user_id == str(current_user.id)
            )
        )
        profile = profile_result.scalar_one_or_none()

        if not profile:
            return {
                "has_profile": False,
                "message": "Complete onboarding to enable personalization",
            }

        # Get chapter personalizations
        chapter_result = await db.execute(
            select(ChapterPersonalization).where(
                ChapterPersonalization.profile_id == profile.id
            )
        )
        chapter_prefs = chapter_result.scalars().all()

        enabled_count = sum(1 for cp in chapter_prefs if cp.is_enabled)
        disabled_count = len(chapter_prefs) - enabled_count

        return {
            "has_profile": True,
            "learning_style": profile.learning_style.value if profile.learning_style else None,
            "learning_pace": profile.learning_pace.value,
            "preferred_language": profile.preferred_language,
            "preferred_domain": profile.preferred_examples_domain,
            "adaptive_complexity": profile.adaptive_complexity,
            "personalized_exercises": profile.personalized_exercises,
            "personalized_time_estimates": profile.personalized_time_estimates,
            "chapter_personalizations": {
                "total": len(chapter_prefs),
                "enabled": enabled_count,
                "disabled": disabled_count,
            },
        }

    except Exception as e:
        logger.error("get_stats_error", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to get personalization stats")
