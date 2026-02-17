"""
Personalization Service
Adapts content based on user preferences and learning profile
Sprint 3: Personalization Engine
"""

from typing import Optional, List, Dict, Any
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import structlog

from src.ai.personalization.models import (
    PersonalizationProfile,
    ChapterPersonalization,
    LearningStyle,
    LearningPace,
)
from src.core.content.models import Content
from src.core.content.enhanced_models import (
    ContentVariant,
    VariantType,
    ComplexityLevel,
)
from src.ai.shared.llm_client import LLMClient

logger = structlog.get_logger()


class PersonalizationService:
    """
    Adapts content based on user profile
    Implements FR-081 to FR-090
    """

    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    async def get_personalized_content(
        self,
        content_id: str,
        user_id: str,
        db: AsyncSession,
    ) -> Optional[ContentVariant]:
        """
        Returns appropriate content variant based on:
        - User's learning style
        - Complexity preference
        - Language preference
        - Domain interest

        FR-082: Per-chapter personalization
        FR-083: Adaptive complexity
        """
        try:
            # Get user profile
            profile = await self._get_user_profile(user_id, db)
            if not profile:
                logger.warning("no_profile_found", user_id=user_id)
                return await self._get_default_variant(content_id, db)

            # Check if personalization is enabled
            if not profile.allow_ai_personalization:
                return await self._get_default_variant(content_id, db)

            # Get chapter-specific personalization settings
            chapter_pref = await self._get_chapter_personalization(
                profile.id, content_id, db
            )
            if chapter_pref and not chapter_pref.is_enabled:
                return await self._get_default_variant(content_id, db)

            # Determine complexity level
            complexity = await self._determine_complexity_level(profile, content_id, db)

            # Get variant matching user preferences
            variant = await self._get_matching_variant(
                content_id=content_id,
                language=profile.preferred_language,
                complexity=complexity,
                db=db,
            )

            if variant:
                logger.info(
                    "personalized_content_served",
                    user_id=user_id,
                    content_id=content_id,
                    variant_type=variant.variant_type,
                    complexity=complexity,
                    language=profile.preferred_language,
                )
                return variant

            # Fallback to default
            return await self._get_default_variant(content_id, db)

        except Exception as e:
            logger.error("personalization_error", error=str(e), user_id=user_id)
            return await self._get_default_variant(content_id, db)

    async def generate_personalized_examples(
        self,
        content: Content,
        profile: PersonalizationProfile,
    ) -> List[Dict[str, Any]]:
        """
        Generate domain-specific examples using LLM
        FR-087: Domain-adjusted examples

        E.g., if user prefers healthcare domain,
        convert generic robot examples to medical robot examples
        """
        if not profile.preferred_examples_domain:
            return []

        try:
            prompt = f"""
You are adapting robotics educational content for a learner interested in {profile.preferred_examples_domain}.

Original content title: {content.title}
Original learning objectives: {content.learning_objectives}

Generate 3 domain-specific examples that:
1. Relate to {profile.preferred_examples_domain}
2. Maintain technical accuracy
3. Are engaging and relevant
4. Match the learning objectives

Format as JSON array:
[
  {{
    "title": "Example title",
    "description": "Brief description",
    "code_snippet": "Optional code example",
    "real_world_application": "How this applies in {profile.preferred_examples_domain}"
  }}
]
"""

            response = await self.llm_client.generate(
                prompt=prompt,
                temperature=0.7,
                max_tokens=1500,
            )

            # Parse JSON response
            import json
            examples = json.loads(response)

            logger.info(
                "personalized_examples_generated",
                content_id=content.id,
                domain=profile.preferred_examples_domain,
                count=len(examples),
            )

            return examples

        except Exception as e:
            logger.error("example_generation_error", error=str(e))
            return []

    async def adjust_complexity(
        self,
        content: Content,
        complexity_level: str,
    ) -> Optional[ContentVariant]:
        """
        Simplify or enhance content complexity
        FR-083: Adaptive complexity

        - Simplified: Remove advanced theory, add more explanations
        - Advanced: Add mathematical proofs, edge cases
        """
        # This would typically trigger content variant generation
        # For now, return None to indicate variant needs to be created
        logger.info(
            "complexity_adjustment_requested",
            content_id=content.id,
            target_complexity=complexity_level,
        )
        return None

    async def estimate_personalized_time(
        self,
        content: Content,
        profile: PersonalizationProfile,
    ) -> int:
        """
        Adjust time estimates based on:
        - User's pace preference
        - Background level
        - Historical completion times

        FR-088: Personalized time estimates
        Returns: estimated minutes
        """
        base_time = content.estimated_reading_time or 30  # Default 30 min

        # Adjust based on learning pace
        pace_multipliers = {
            LearningPace.SLOW: 1.5,
            LearningPace.MODERATE: 1.0,
            LearningPace.FAST: 0.7,
        }

        multiplier = pace_multipliers.get(profile.learning_pace, 1.0)

        # Adjust based on background
        if profile.prior_experience:
            # Users with experience might go faster
            multiplier *= 0.9

        estimated_time = int(base_time * multiplier)

        logger.debug(
            "time_estimate_calculated",
            content_id=content.id,
            base_time=base_time,
            multiplier=multiplier,
            estimated_time=estimated_time,
        )

        return estimated_time

    async def _get_user_profile(
        self, user_id: str, db: AsyncSession
    ) -> Optional[PersonalizationProfile]:
        """Fetch user's personalization profile"""
        result = await db.execute(
            select(PersonalizationProfile).where(
                PersonalizationProfile.user_id == user_id
            )
        )
        return result.scalar_one_or_none()

    async def _get_chapter_personalization(
        self, profile_id: UUID, content_id: str, db: AsyncSession
    ) -> Optional[ChapterPersonalization]:
        """Get chapter-specific personalization settings"""
        result = await db.execute(
            select(ChapterPersonalization).where(
                ChapterPersonalization.profile_id == profile_id,
                ChapterPersonalization.content_id == content_id,
            )
        )
        return result.scalar_one_or_none()

    async def _determine_complexity_level(
        self, profile: PersonalizationProfile, content_id: str, db: AsyncSession
    ) -> ComplexityLevel:
        """
        Determine appropriate complexity level based on:
        - User's background
        - Learning pace
        - Historical performance
        """
        # Default to intermediate
        complexity = ComplexityLevel.INTERMEDIATE

        # Adjust based on background
        if profile.educational_background:
            background_lower = profile.educational_background.lower()
            if any(
                term in background_lower
                for term in ["phd", "master", "advanced", "expert"]
            ):
                complexity = ComplexityLevel.ADVANCED
            elif any(
                term in background_lower for term in ["beginner", "new", "learning"]
            ):
                complexity = ComplexityLevel.BEGINNER

        # Adjust based on pace
        if profile.learning_pace == LearningPace.FAST:
            if complexity == ComplexityLevel.INTERMEDIATE:
                complexity = ComplexityLevel.ADVANCED
        elif profile.learning_pace == LearningPace.SLOW:
            if complexity == ComplexityLevel.INTERMEDIATE:
                complexity = ComplexityLevel.BEGINNER

        return complexity

    async def _get_matching_variant(
        self,
        content_id: str,
        language: str,
        complexity: ComplexityLevel,
        db: AsyncSession,
    ) -> Optional[ContentVariant]:
        """Find content variant matching user preferences"""
        result = await db.execute(
            select(ContentVariant).where(
                ContentVariant.content_id == content_id,
                ContentVariant.language_code == language,
                ContentVariant.complexity_level == complexity,
            )
        )
        return result.scalar_one_or_none()

    async def _get_default_variant(
        self, content_id: str, db: AsyncSession
    ) -> Optional[ContentVariant]:
        """Get default content variant (standard, English)"""
        result = await db.execute(
            select(ContentVariant).where(
                ContentVariant.content_id == content_id,
                ContentVariant.variant_type == VariantType.STANDARD,
                ContentVariant.language_code == "en",
            )
        )
        return result.scalar_one_or_none()
