"""
AI Tutor Pydantic Schemas
Request/Response models for API endpoints
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID

from .models import IntentType, GuardrailType


# ============================================================================
# Request Schemas
# ============================================================================

class CreateTutorConversationRequest(BaseModel):
    """Request to start a new AI tutor conversation"""
    stage_id: Optional[UUID] = Field(None, description="Stage context for conversation")
    content_id: Optional[UUID] = Field(None, description="Content context for conversation")
    initial_message: str = Field(..., min_length=1, max_length=5000, description="First message from student")
    code_snippet: Optional[str] = Field(None, description="Code to discuss (if applicable)")


class SendTutorMessageRequest(BaseModel):
    """Request to send a message in tutor conversation"""
    content: str = Field(..., min_length=1, max_length=5000, description="Student message")
    code_snippet: Optional[str] = Field(None, description="Code to review or debug")
    understanding_level: Optional[int] = Field(None, ge=1, le=5, description="Self-reported understanding (1-5)")


class CodeReviewRequest(BaseModel):
    """Request for AI tutor code review (FR-031)"""
    conversation_id: Optional[UUID] = Field(None, description="Existing conversation or create new")
    code: str = Field(..., min_length=1, description="Code to review")
    language: str = Field(..., description="Programming language")
    context: Optional[str] = Field(None, description="What the code is supposed to do")
    stage_id: Optional[UUID] = Field(None, description="Current learning stage")


class DebuggingHelpRequest(BaseModel):
    """Request for systematic debugging guidance (FR-030)"""
    conversation_id: Optional[UUID] = Field(None, description="Existing conversation or create new")
    code: str = Field(..., min_length=1, description="Code with issue")
    error_message: Optional[str] = Field(None, description="Error message if any")
    expected_behavior: str = Field(..., description="What should happen")
    actual_behavior: str = Field(..., description="What actually happens")
    stage_id: Optional[UUID] = Field(None, description="Current learning stage")


class EscalateToInstructorRequest(BaseModel):
    """Request to escalate to human instructor (FR-035)"""
    conversation_id: UUID = Field(..., description="Conversation to escalate")
    reason: str = Field(..., min_length=10, max_length=500, description="Reason for escalation")


# ============================================================================
# Response Schemas
# ============================================================================

class GuardrailEventResponse(BaseModel):
    """Guardrail event information"""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    guardrail_type: GuardrailType
    trigger_reason: str
    escalated: bool
    created_at: datetime


class AIMessageResponse(BaseModel):
    """AI tutor message response"""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    role: str
    content: str
    response_type: Optional[str] = None
    socratic_strategy: Optional[str] = None
    provided_hints: Optional[List[str]] = None
    code_issues: Optional[List[Dict[str, Any]]] = None
    debugging_steps: Optional[List[str]] = None
    confidence_score: Optional[float] = None
    created_at: datetime


class AIConversationResponse(BaseModel):
    """AI tutor conversation response"""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    stage_id: Optional[UUID] = None
    content_id: Optional[UUID] = None
    title: str
    intent_type: Optional[IntentType] = None
    created_at: datetime
    updated_at: datetime
    messages: List[AIMessageResponse] = []
    recent_guardrails: List[GuardrailEventResponse] = []


class TutorResponseDTO(BaseModel):
    """Structured tutor response with metadata"""
    message_id: UUID
    conversation_id: UUID
    content: str
    response_type: str  # 'socratic_question', 'hint', 'guidance', 'explanation', 'code_review'

    # Socratic elements (FR-027)
    guiding_questions: Optional[List[str]] = None
    hints: Optional[List[str]] = None

    # Code feedback (FR-031)
    code_issues: Optional[List[Dict[str, Any]]] = None  # [{line, type, message, hint}]

    # Debugging guidance (FR-030)
    debugging_steps: Optional[List[str]] = None
    systematic_approach: Optional[str] = None

    # Guardrail information
    guardrail_triggered: bool = False
    guardrail_message: Optional[str] = None

    # Understanding adaptation (FR-029)
    adapted_for_level: Optional[int] = None
    explanation_depth: Optional[str] = None  # 'basic', 'intermediate', 'advanced'

    # Escalation option (FR-035)
    escalation_available: bool = False
    escalation_reason: Optional[str] = None


class DebuggingGuidanceDTO(BaseModel):
    """Systematic debugging guidance (FR-030)"""
    message_id: UUID
    conversation_id: UUID

    # Systematic methodology
    observation: str  # What we observe from error/behavior
    hypothesis: List[str]  # Possible causes
    verification_steps: List[Dict[str, str]]  # {step, action, expected_result}

    # Hints without solutions
    hints: List[str]
    guiding_questions: List[str]

    # Resources
    relevant_concepts: List[str]
    documentation_links: Optional[List[Dict[str, str]]] = None  # {title, url}


class CodeReviewDTO(BaseModel):
    """Code review feedback without auto-fix (FR-031)"""
    message_id: UUID
    conversation_id: UUID

    # Identified issues
    issues: List[Dict[str, Any]]  # {line, severity, category, description, hint}

    # Positive feedback
    strengths: List[str]

    # Guiding questions for improvement
    improvement_questions: List[str]

    # Conceptual guidance
    concepts_to_review: List[str]
    best_practices: List[str]

    # No direct solutions (FR-028)
    solution_provided: bool = False


class EscalationResponse(BaseModel):
    """Escalation confirmation (FR-035)"""
    conversation_id: UUID
    escalated_at: datetime
    instructor_notified: bool
    estimated_response_time: str
    reference_number: str
