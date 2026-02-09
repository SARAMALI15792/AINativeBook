"""
AI Tutor Database Models
FR-026 to FR-035: Socratic AI Tutor with Guardrails
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, JSON, Integer, Float, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import enum

from ...shared.database import Base


class IntentType(str, enum.Enum):
    """Types of user intents (FR-028, FR-029)"""
    CONCEPT = "concept"  # Conceptual question
    CODE = "code"  # Code writing help
    DEBUG = "debug"  # Debugging assistance
    DIRECT_ANSWER = "direct_answer"  # Direct answer request (blocked)
    CODE_REVIEW = "code_review"  # Code review request
    EXPLANATION = "explanation"  # Explanation request


class GuardrailType(str, enum.Enum):
    """Types of guardrail triggers (FR-027, FR-028)"""
    SOCRATIC_REDIRECT = "socratic_redirect"  # Redirected to guiding question
    CODE_SOLUTION_BLOCKED = "code_solution_blocked"  # Prevented direct code solution
    ESCALATION_TRIGGERED = "escalation_triggered"  # Escalated to instructor
    UNDERSTANDING_CHECK = "understanding_check"  # Understanding verification
    HINT_ONLY = "hint_only"  # Provided hint without solution


class AIConversation(Base):
    """
    AI Tutor conversation tracking
    FR-033: Store interactions for 30 days
    FR-034: Maintain conversation context
    """
    __tablename__ = "ai_conversations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    stage_id = Column(UUID(as_uuid=True), ForeignKey("stages.id", ondelete="SET NULL"), nullable=True)
    content_id = Column(UUID(as_uuid=True), ForeignKey("content_items.id", ondelete="SET NULL"), nullable=True)

    title = Column(String(255), nullable=False)  # Auto-generated from first message
    intent_type = Column(SQLEnum(IntentType), nullable=True)  # Primary intent of conversation

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=True)  # FR-033: 30-day retention

    # Relationships
    user = relationship("User", back_populates="ai_conversations")
    stage = relationship("Stage", back_populates="ai_conversations")
    content = relationship("ContentItem", back_populates="ai_conversations")
    messages = relationship("AIMessage", back_populates="conversation", cascade="all, delete-orphan")
    guardrail_events = relationship("GuardrailEvent", back_populates="conversation", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<AIConversation(id={self.id}, user_id={self.user_id}, title='{self.title}')>"


class AIMessage(Base):
    """
    Individual messages in AI tutor conversations
    FR-027: Track Socratic interactions
    FR-029: Store stage-appropriate responses
    """
    __tablename__ = "ai_messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("ai_conversations.id", ondelete="CASCADE"), nullable=False)

    role = Column(String(20), nullable=False)  # 'user' or 'assistant'
    content = Column(Text, nullable=False)  # The actual message text

    # User message metadata
    user_query = Column(Text, nullable=True)  # Original user query before guardrails
    detected_intent = Column(SQLEnum(IntentType), nullable=True)  # Detected intent
    understanding_level = Column(Integer, nullable=True)  # Estimated 1-5 (FR-029)

    # Assistant response metadata
    response_type = Column(String(50), nullable=True)  # 'socratic_question', 'hint', 'guidance', 'explanation'
    socratic_strategy = Column(String(100), nullable=True)  # Strategy used (e.g., 'decompose_problem', 'analogy')
    provided_hints = Column(JSON, nullable=True)  # List of hints given

    # Code-related metadata (FR-030, FR-031)
    code_snippet = Column(Text, nullable=True)  # Code submitted by user
    code_issues = Column(JSON, nullable=True)  # Issues identified in code
    debugging_steps = Column(JSON, nullable=True)  # Systematic debugging steps suggested

    # Quality metrics
    response_time_ms = Column(Integer, nullable=True)  # Response generation time
    confidence_score = Column(Float, nullable=True)  # Confidence in response (0-1)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    conversation = relationship("AIConversation", back_populates="messages")

    def __repr__(self):
        return f"<AIMessage(id={self.id}, role='{self.role}', conversation_id={self.conversation_id})>"


class GuardrailEvent(Base):
    """
    Tracks when guardrails are triggered
    FR-027: Socratic method enforcement
    FR-028: Refuse direct code solutions
    FR-035: Escalation logging
    """
    __tablename__ = "guardrail_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("ai_conversations.id", ondelete="CASCADE"), nullable=False)
    message_id = Column(UUID(as_uuid=True), ForeignKey("ai_messages.id", ondelete="CASCADE"), nullable=True)

    guardrail_type = Column(SQLEnum(GuardrailType), nullable=False)
    trigger_reason = Column(Text, nullable=False)  # Why guardrail was triggered
    original_request = Column(Text, nullable=True)  # What user originally asked for
    modified_response = Column(Text, nullable=True)  # How response was modified

    # Escalation metadata (FR-035)
    escalated = Column(Boolean, default=False)  # Whether escalated to instructor
    escalation_reason = Column(Text, nullable=True)  # Why escalation happened
    instructor_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    # Analysis metadata
    severity = Column(String(20), nullable=True)  # 'low', 'medium', 'high'
    action_taken = Column(String(100), nullable=True)  # Action taken by guardrail

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    conversation = relationship("AIConversation", back_populates="guardrail_events")
    message = relationship("AIMessage")
    instructor = relationship("User", foreign_keys=[instructor_id])

    def __repr__(self):
        return f"<GuardrailEvent(id={self.id}, type='{self.guardrail_type}', escalated={self.escalated})>"
