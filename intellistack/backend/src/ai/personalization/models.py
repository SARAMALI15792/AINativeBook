"""
Personalization Database Models
FR-081 to FR-090: User profiles, preferences, adaptive learning
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, JSON, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import enum

from ...shared.database import Base


class LearningStyle(str, enum.Enum):
    """Learning style preferences"""
    VISUAL = "visual"  # Visual learners
    AUDITORY = "auditory"  # Audio learners
    KINESTHETIC = "kinesthetic"  # Hands-on learners
    READING = "reading"  # Reading/writing learners


class LearningPace(str, enum.Enum):
    """Learning pace preferences"""
    SLOW = "slow"  # Extra time and explanation
    MODERATE = "moderate"  # Standard pace
    FAST = "fast"  # Accelerated content


class PersonalizationProfile(Base):
    """
    User personalization profile
    FR-081: Background profile collection
    FR-089: Personalization reset option
    """
    __tablename__ = "personalization_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)

    # Background information (FR-081)
    educational_background = Column(String(255), nullable=True)  # e.g., "Computer Science degree"
    prior_experience = Column(Text, nullable=True)  # Previous experience with robotics/AI
    technical_skills = Column(JSON, nullable=True)  # ["Python", "Linux", "ROS"]
    learning_goals = Column(Text, nullable=True)  # What they want to achieve

    # Learning preferences
    learning_style = Column(SQLEnum(LearningStyle), nullable=True)
    learning_pace = Column(SQLEnum(LearningPace), default=LearningPace.MODERATE)
    preferred_language = Column(String(10), default="en")  # 'en' or 'ur' (FR-084)

    # Domain-specific preferences (FR-087)
    preferred_examples_domain = Column(String(100), nullable=True)  # e.g., "healthcare", "manufacturing"
    interest_areas = Column(JSON, nullable=True)  # ["computer_vision", "manipulation", "navigation"]

    # Adaptation settings (FR-083)
    adaptive_complexity = Column(Boolean, default=True)  # Enable adaptive content complexity
    personalized_exercises = Column(Boolean, default=True)  # Generate personalized exercises (FR-086)
    personalized_time_estimates = Column(Boolean, default=True)  # Show personalized time estimates (FR-088)

    # Privacy settings (FR-090)
    share_progress_with_instructors = Column(Boolean, default=True)
    share_with_peers = Column(Boolean, default=False)
    allow_ai_personalization = Column(Boolean, default=True)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_reset_at = Column(DateTime, nullable=True)  # FR-089: Reset tracking

    # Relationships
    user = relationship("User", back_populates="personalization_profile")
    chapter_personalizations = relationship(
        "ChapterPersonalization",
        back_populates="profile",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<PersonalizationProfile(user_id={self.user_id}, style='{self.learning_style}')>"


class ChapterPersonalization(Base):
    """
    Per-chapter personalization settings
    FR-082: Per-chapter personalization button
    """
    __tablename__ = "chapter_personalizations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    profile_id = Column(UUID(as_uuid=True), ForeignKey("personalization_profiles.id", ondelete="CASCADE"), nullable=False)
    content_id = Column(UUID(as_uuid=True), ForeignKey("content_items.id", ondelete="CASCADE"), nullable=False)

    # Personalization state
    is_enabled = Column(Boolean, default=True)
    complexity_level = Column(String(20), nullable=True)  # 'basic', 'intermediate', 'advanced'

    # Applied adaptations
    applied_examples = Column(JSON, nullable=True)  # Domain-adjusted examples used (FR-087)
    simplified_concepts = Column(JSON, nullable=True)  # Concepts simplified
    additional_resources = Column(JSON, nullable=True)  # Extra resources provided

    # Tracking
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    profile = relationship("PersonalizationProfile", back_populates="chapter_personalizations")
    content = relationship("ContentItem")

    def __repr__(self):
        return f"<ChapterPersonalization(profile_id={self.profile_id}, content_id={self.content_id})>"


class TranslationCache(Base):
    """
    Cached translations for performance
    FR-084: Urdu translation toggle
    """
    __tablename__ = "translation_cache"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    source_language = Column(String(10), nullable=False, default="en")
    target_language = Column(String(10), nullable=False)  # 'ur' for Urdu

    # Content identification
    content_type = Column(String(50), nullable=False)  # 'chapter', 'exercise', 'quiz_question'
    content_id = Column(UUID(as_uuid=True), nullable=False)

    # Translation
    original_text = Column(Text, nullable=False)
    translated_text = Column(Text, nullable=False)

    # Metadata
    translation_model = Column(String(100), nullable=True)  # Model used for translation
    quality_score = Column(String(20), nullable=True)  # 'high', 'medium', 'low'

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=True)  # Cache expiration

    def __repr__(self):
        return f"<TranslationCache({self.source_language}→{self.target_language}, content_id={self.content_id})>"
