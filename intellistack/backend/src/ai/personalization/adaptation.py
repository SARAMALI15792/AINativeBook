"""
Content Adaptation Service
FR-082: Per-chapter personalization button
FR-083: Adaptive content complexity
FR-086: Personalized exercise variations
FR-087: Domain-adjusted examples
"""

import uuid
from typing import Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .models import PersonalizationProfile, ChapterPersonalization
from .profile import ProfileService


class AdaptationService:
    """Service for adapting content to user preferences"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.profile_service = ProfileService(db)

    async def enable_chapter_personalization(
        self, user_id: uuid.UUID, content_id: uuid.UUID
    ) -> ChapterPersonalization:
        """
        Enable personalization for a specific chapter (FR-082)
        """
        # Get profile
        profile = await self.profile_service.get_or_create_profile(user_id)

        # Check if personalization already exists
        query = select(ChapterPersonalization).where(
            ChapterPersonalization.profile_id == profile.id,
            ChapterPersonalization.content_id == content_id,
        )
        result = await self.db.execute(query)
        chapter_personalization = result.scalar_one_or_none()

        if not chapter_personalization:
            chapter_personalization = ChapterPersonalization(
                profile_id=profile.id,
                content_id=content_id,
                is_enabled=True,
            )
            self.db.add(chapter_personalization)
        else:
            chapter_personalization.is_enabled = True

        await self.db.commit()
        await self.db.refresh(chapter_personalization)

        return chapter_personalization

    async def adapt_content_complexity(
        self, user_id: uuid.UUID, content: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Adapt content complexity based on user profile (FR-083)
        """
        # Get complexity level
        complexity = await self.profile_service.get_complexity_level(user_id)

        # Adapt content
        adapted = content.copy()
        adapted["complexity_level"] = complexity

        if complexity == "basic":
            adapted["explanation_depth"] = "detailed"
            adapted["include_prerequisites"] = True
            adapted["include_analogies"] = True
        elif complexity == "advanced":
            adapted["explanation_depth"] = "concise"
            adapted["include_prerequisites"] = False
            adapted["include_advanced_topics"] = True
        else:  # intermediate
            adapted["explanation_depth"] = "standard"
            adapted["include_prerequisites"] = False

        return adapted

    async def generate_personalized_exercise(
        self, user_id: uuid.UUID, base_exercise: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate personalized exercise variation (FR-086)

        In production: Use AI to generate variations
        """
        profile = await self.profile_service.get_or_create_profile(user_id)

        if not await self.profile_service.should_generate_personalized_exercise(user_id):
            return base_exercise

        # Create variation based on profile
        personalized = base_exercise.copy()

        # Adjust difficulty based on pace
        if profile.learning_pace == "slow":
            personalized["difficulty"] = "easy"
            personalized["hints_available"] = True
            personalized["step_by_step_guide"] = True
        elif profile.learning_pace == "fast":
            personalized["difficulty"] = "challenging"
            personalized["bonus_objectives"] = True

        # Adjust domain if specified
        if profile.preferred_examples_domain:
            personalized["domain_context"] = profile.preferred_examples_domain

        return personalized

    async def adjust_examples_to_domain(
        self, user_id: uuid.UUID, examples: List[str]
    ) -> List[str]:
        """
        Adjust examples to user's preferred domain (FR-087)

        In production: Use AI to transform examples
        """
        profile = await self.profile_service.get_or_create_profile(user_id)

        if not profile.preferred_examples_domain:
            return examples

        # Placeholder: In production, use AI to transform examples
        # For now, add domain context to examples
        domain = profile.preferred_examples_domain
        adjusted = []

        for example in examples:
            adjusted.append(f"[{domain.title()} Context] {example}")

        return adjusted

    async def get_personalized_learning_path(
        self, user_id: uuid.UUID, content_ids: List[uuid.UUID]
    ) -> List[uuid.UUID]:
        """
        Personalize learning path based on interests and background

        In production: Use AI to recommend optimal path
        """
        profile = await self.profile_service.get_or_create_profile(user_id)

        # If no interest areas, return default path
        if not profile.interest_areas:
            return content_ids

        # Placeholder: In production, reorder based on interests
        # For now, return default order
        return content_ids

    async def get_adaptive_resources(
        self, user_id: uuid.UUID, topic: str
    ) -> List[Dict[str, str]]:
        """
        Get adaptive resources based on learning style
        """
        profile = await self.profile_service.get_or_create_profile(user_id)

        resources = []

        if profile.learning_style == "visual":
            resources.extend([
                {"type": "video", "title": f"{topic} - Video Tutorial"},
                {"type": "diagram", "title": f"{topic} - Visual Diagrams"},
            ])
        elif profile.learning_style == "auditory":
            resources.extend([
                {"type": "podcast", "title": f"{topic} - Audio Explanation"},
                {"type": "lecture", "title": f"{topic} - Lecture Recording"},
            ])
        elif profile.learning_style == "kinesthetic":
            resources.extend([
                {"type": "lab", "title": f"{topic} - Hands-on Lab"},
                {"type": "simulation", "title": f"{topic} - Interactive Simulation"},
            ])
        else:  # reading
            resources.extend([
                {"type": "article", "title": f"{topic} - In-depth Article"},
                {"type": "documentation", "title": f"{topic} - Technical Documentation"},
            ])

        return resources
