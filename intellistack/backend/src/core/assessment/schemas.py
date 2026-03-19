"""
Assessment Pydantic Schemas
Request/Response models for assessment API
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID

from .models import AssessmentType, QuestionType, SubmissionStatus


# ============================================================================
# Request Schemas
# ============================================================================

class CreateAssessmentRequest(BaseModel):
    """Request to create an assessment"""
    stage_id: UUID
    content_id: Optional[UUID] = None
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    assessment_type: AssessmentType
    passing_score: float = Field(70.0, ge=0, le=100)
    time_limit_minutes: Optional[int] = Field(None, gt=0)
    max_attempts: Optional[int] = Field(None, gt=0)
    is_required: bool = True
    is_safety_assessment: bool = False
    available_from: Optional[datetime] = None
    available_until: Optional[datetime] = None


class CreateQuestionRequest(BaseModel):
    """Request to add question to assessment"""
    question_text: str = Field(..., min_length=1)
    question_type: QuestionType
    points: float = Field(1.0, gt=0)
    order_index: int = Field(0, ge=0)
    options: Optional[List[Dict[str, Any]]] = None  # For multiple choice
    starter_code: Optional[str] = None  # For code questions
    test_cases: Optional[List[Dict[str, str]]] = None  # For code questions
    correct_answer: Optional[str] = None
    explanation: Optional[str] = None


class SubmitAnswersRequest(BaseModel):
    """Request to submit assessment answers"""
    answers: Dict[str, Any] = Field(..., description="question_id: answer mapping")


class GradeSubmissionRequest(BaseModel):
    """Request to grade a submission (instructor)"""
    score: float = Field(..., ge=0, le=100)
    feedback: Optional[str] = None
    rubric_scores: Optional[List[Dict[str, Any]]] = None


class CreatePeerReviewRequest(BaseModel):
    """Request to create peer review"""
    submission_id: UUID
    rating: Optional[int] = Field(None, ge=1, le=5)
    strengths: Optional[str] = None
    areas_for_improvement: Optional[str] = None
    overall_feedback: Optional[str] = None
    rubric_scores: Optional[Dict[str, Any]] = None


class CreateRubricRequest(BaseModel):
    """Request to create rubric"""
    title: str
    description: Optional[str] = None
    criteria: List[Dict[str, Any]]  # See Rubric model for structure


# ============================================================================
# Response Schemas
# ============================================================================

class QuestionResponse(BaseModel):
    """Assessment question response"""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    question_text: str
    question_type: QuestionType
    points: float
    order_index: int
    options: Optional[List[Dict[str, Any]]] = None
    starter_code: Optional[str] = None
    # Hide correct_answer and test_cases from students


class AssessmentResponse(BaseModel):
    """Assessment response"""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    stage_id: UUID
    content_id: Optional[UUID] = None
    title: str
    description: Optional[str] = None
    assessment_type: AssessmentType
    passing_score: float
    time_limit_minutes: Optional[int] = None
    max_attempts: Optional[int] = None
    is_required: bool
    is_safety_assessment: bool
    available_from: Optional[datetime] = None
    available_until: Optional[datetime] = None
    created_at: datetime
    questions: List[QuestionResponse] = []


class SubmissionResponse(BaseModel):
    """Submission response"""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    assessment_id: UUID
    user_id: UUID
    status: SubmissionStatus
    attempt_number: int
    score: Optional[float] = None
    total_points: Optional[float] = None
    earned_points: Optional[float] = None
    passed: Optional[bool] = None
    auto_graded: bool
    graded_at: Optional[datetime] = None
    feedback: Optional[str] = None
    similarity_score: Optional[float] = None
    flagged_for_review: bool
    started_at: Optional[datetime] = None
    submitted_at: Optional[datetime] = None
    time_spent_minutes: Optional[int] = None
    created_at: datetime


class RubricResponse(BaseModel):
    """Rubric response"""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    assessment_id: UUID
    title: str
    description: Optional[str] = None
    criteria: List[Dict[str, Any]]
    created_at: datetime


class PeerReviewResponse(BaseModel):
    """Peer review response"""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    submission_id: UUID
    reviewer_id: UUID
    rating: Optional[int] = None
    strengths: Optional[str] = None
    areas_for_improvement: Optional[str] = None
    overall_feedback: Optional[str] = None
    rubric_scores: Optional[Dict[str, Any]] = None
    completed: bool
    submitted_at: Optional[datetime] = None
    created_at: datetime


class AssessmentResultDTO(BaseModel):
    """Detailed assessment result for student"""
    submission: SubmissionResponse
    assessment: AssessmentResponse
    answers_with_feedback: List[Dict[str, Any]]  # Question, student answer, correct answer, explanation
    passed: bool
    attempts_remaining: Optional[int] = None
    can_retake: bool


class GradingFeedbackDTO(BaseModel):
    """Feedback for graded submission"""
    submission_id: UUID
    score: float
    passed: bool
    feedback: str
    rubric_scores: Optional[List[Dict[str, Any]]] = None
    strengths: List[str]
    areas_for_improvement: List[str]
