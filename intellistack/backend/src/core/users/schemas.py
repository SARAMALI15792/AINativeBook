"""User schemas for onboarding and preferences."""

from typing import Optional, List
from pydantic import BaseModel, Field


class SystemPreferences(BaseModel):
    """System/environment preferences."""
    theme: str = Field(default="system", description="Color theme preference")
    os: str = Field(default="other", description="Operating system")
    device_type: str = Field(default="desktop", description="Device type")
    preferred_ide: str = Field(default="vscode", description="Preferred IDE")
    shell_type: str = Field(default="bash", description="Shell type")


class LearningPreferences(BaseModel):
    """Learning style preferences."""
    learning_style: str = Field(default="hands-on", description="Preferred learning style")
    pace_preference: str = Field(default="self-paced", description="Learning pace")
    goal_timeframe: str = Field(default="6-months", description="Goal completion timeframe")
    focus_areas: List[str] = Field(default_factory=list, description="Areas of focus")


class BackgroundLevel(BaseModel):
    """User's background and experience level."""
    programming_experience: str = Field(default="beginner", description="Programming experience level")
    robotics_experience: str = Field(default="none", description="Robotics experience level")
    math_background: str = Field(default="basic", description="Math background level")
    linux_familiarity: str = Field(default="none", description="Linux familiarity level")


class OnboardingData(BaseModel):
    """Complete onboarding data."""
    system_preferences: SystemPreferences = Field(default_factory=SystemPreferences)
    learning_preferences: LearningPreferences = Field(default_factory=LearningPreferences)
    background_level: BackgroundLevel = Field(default_factory=BackgroundLevel)


class UserPreferences(BaseModel):
    """User preferences stored in database."""
    system: Optional[SystemPreferences] = None
    learning: Optional[LearningPreferences] = None
    background: Optional[BackgroundLevel] = None
    onboarding_completed: bool = False
    onboarding_completed_at: Optional[str] = None


class UserProfileResponse(BaseModel):
    """User profile response."""
    id: str
    email: str
    name: Optional[str] = None
    role: str = "student"
    email_verified: bool = False
    preferences: Optional[UserPreferences] = None
    current_stage: int = 1
