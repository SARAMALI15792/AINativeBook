"""
Personalization Profile Service
FR-081: Background profile collection
FR-089: Personalization reset
"""

import uuid
from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .models import PersonalizationProfile, LearningStyle, LearningPace


class ProfileService:
    """Service for managing personalization profiles"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_or_create_profile(self, user_id: uuid.UUID) -> PersonalizationProfile:
        """
        Get existing profile or create new one (FR-081)
        """
        query = select(PersonalizationProfile).where(PersonalizationProfile.user_id == user_id)
        result = await self.db.execute(query)
        profile = result.scalar_one_or_none()

        if not profile:
            profile = PersonalizationProfile(user_id=user_id)
            self.db.add(profile)
            await self.db.commit()
            await self.db.refresh(profile)

        return profile

    async def update_profile(
        self,
        user_id: uuid.UUID,
        educational_background: Optional[str] = None,
        prior_experience: Optional[str] = None,
        technical_skills: Optional[list] = None,
        learning_goals: Optional[str] = None,
        learning_style: Optional[LearningStyle] = None,
        learning_pace: Optional[LearningPace] = None,
        preferred_language: Optional[str] = None,
        preferred_examples_domain: Optional[str] = None,
        interest_areas: Optional[list] = None,
    ) -> PersonalizationProfile:
        """
        Update profile with user preferences (FR-081)
        """
        profile = await self.get_or_create_profile(user_id)

        # Update fields if provided
        if educational_background is not None:
            profile.educational_background = educational_background
        if prior_experience is not None:
            profile.prior_experience = prior_experience
        if technical_skills is not None:
            profile.technical_skills = technical_skills
        if learning_goals is not None:
            profile.learning_goals = learning_goals
        if learning_style is not None:
            profile.learning_style = learning_style
        if learning_pace is not None:
            profile.learning_pace = learning_pace
        if preferred_language is not None:
            profile.preferred_language = preferred_language
        if preferred_examples_domain is not None:
            profile.preferred_examples_domain = preferred_examples_domain
        if interest_areas is not None:
            profile.interest_areas = interest_areas

        profile.updated_at = datetime.utcnow()
        await self.db.commit()
        await self.db.refresh(profile)

        return profile

    async def update_preferences(
        self,
        user_id: uuid.UUID,
        adaptive_complexity: Optional[bool] = None,
        personalized_exercises: Optional[bool] = None,
        personalized_time_estimates: Optional[bool] = None,
    ) -> PersonalizationProfile:
        """
        Update personalization preferences (FR-083, FR-086, FR-088)
        """
        profile = await self.get_or_create_profile(user_id)

        if adaptive_complexity is not None:
            profile.adaptive_complexity = adaptive_complexity
        if personalized_exercises is not None:
            profile.personalized_exercises = personalized_exercises
        if personalized_time_estimates is not None:
            profile.personalized_time_estimates = personalized_time_estimates

        profile.updated_at = datetime.utcnow()
        await self.db.commit()
        await self.db.refresh(profile)

        return profile

    async def update_privacy_settings(
        self,
        user_id: uuid.UUID,
        share_progress_with_instructors: Optional[bool] = None,
        share_with_peers: Optional[bool] = None,
        allow_ai_personalization: Optional[bool] = None,
    ) -> PersonalizationProfile:
        """
        Update privacy settings (FR-090)
        """
        profile = await self.get_or_create_profile(user_id)

        if share_progress_with_instructors is not None:
            profile.share_progress_with_instructors = share_progress_with_instructors
        if share_with_peers is not None:
            profile.share_with_peers = share_with_peers
        if allow_ai_personalization is not None:
            profile.allow_ai_personalization = allow_ai_personalization

        profile.updated_at = datetime.utcnow()
        await self.db.commit()
        await self.db.refresh(profile)

        return profile

    async def reset_personalization(self, user_id: uuid.UUID) -> PersonalizationProfile:
        """
        Reset personalization to defaults (FR-089)
        """
        profile = await self.get_or_create_profile(user_id)

        # Reset to defaults
        profile.learning_style = None
        profile.learning_pace = LearningPace.MODERATE
        profile.preferred_language = "en"
        profile.preferred_examples_domain = None
        profile.interest_areas = None
        profile.adaptive_complexity = True
        profile.personalized_exercises = True
        profile.personalized_time_estimates = True
        profile.last_reset_at = datetime.utcnow()
        profile.updated_at = datetime.utcnow()

        await self.db.commit()
        await self.db.refresh(profile)

        return profile

    async def get_complexity_level(self, user_id: uuid.UUID) -> str:
        """
        Get appropriate complexity level based on profile (FR-083)
        """
        profile = await self.get_or_create_profile(user_id)

        if not profile.adaptive_complexity:
            return "intermediate"  # Default

        # Determine complexity based on background and pace
        if profile.learning_pace == LearningPace.FAST and profile.prior_experience:
            return "advanced"
        elif profile.learning_pace == LearningPace.SLOW or not profile.prior_experience:
            return "basic"
        else:
            return "intermediate"

    async def get_personalized_time_estimate(
        self, user_id: uuid.UUID, base_time_minutes: int
    ) -> int:
        """
        Calculate personalized time estimate (FR-088)
        """
        profile = await self.get_or_create_profile(user_id)

        if not profile.personalized_time_estimates:
            return base_time_minutes

        # Adjust based on learning pace
        if profile.learning_pace == LearningPace.SLOW:
            return int(base_time_minutes * 1.5)  # 50% more time
        elif profile.learning_pace == LearningPace.FAST:
            return int(base_time_minutes * 0.75)  # 25% less time
        else:
            return base_time_minutes

    async def should_generate_personalized_exercise(self, user_id: uuid.UUID) -> bool:
        """
        Check if personalized exercises should be generated (FR-086)
        """
        profile = await self.get_or_create_profile(user_id)
        return profile.personalized_exercises and profile.allow_ai_personalization
