"""
AI Tutor Service Layer
Integrates agents, guardrails, and database
FR-026 to FR-035
"""

import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload

from ...shared.database import get_db
from ...core.auth.models import User
from ...core.learning.models import Stage, ContentItem
from .models import AIConversation, AIMessage, GuardrailEvent, IntentType, GuardrailType
from .schemas import (
    TutorResponseDTO,
    DebuggingGuidanceDTO,
    CodeReviewDTO,
    EscalationResponse,
)
from .agents import create_tutor_agent, run_tutor_conversation
from .guardrails import enforce_guardrails, validate_ai_response, GuardrailViolation


class AITutorService:
    """Service for AI tutor operations"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_conversation(
        self,
        user_id: uuid.UUID,
        stage_id: Optional[uuid.UUID] = None,
        content_id: Optional[uuid.UUID] = None,
        initial_message: str = "New conversation",
    ) -> AIConversation:
        """
        Create a new AI tutor conversation
        FR-033: Conversations stored for 30 days
        """
        conversation = AIConversation(
            user_id=user_id,
            stage_id=stage_id,
            content_id=content_id,
            title=initial_message[:100] if len(initial_message) > 100 else initial_message,
            expires_at=datetime.utcnow() + timedelta(days=30),  # FR-033
        )
        self.db.add(conversation)
        await self.db.commit()
        await self.db.refresh(conversation)
        return conversation

    async def get_conversation(
        self, conversation_id: uuid.UUID, user_id: uuid.UUID
    ) -> Optional[AIConversation]:
        """Get conversation with messages"""
        query = (
            select(AIConversation)
            .options(selectinload(AIConversation.messages))
            .where(
                and_(
                    AIConversation.id == conversation_id,
                    AIConversation.user_id == user_id,
                )
            )
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def send_message(
        self,
        conversation_id: uuid.UUID,
        user_id: uuid.UUID,
        content: str,
        code_snippet: Optional[str] = None,
        understanding_level: Optional[int] = None,
    ) -> TutorResponseDTO:
        """
        Send message to AI tutor and get Socratic response
        FR-027: Socratic method
        FR-028: No direct solutions
        FR-030, FR-031: Specialized guidance
        """
        start_time = datetime.utcnow()

        # Get conversation
        conversation = await self.get_conversation(conversation_id, user_id)
        if not conversation:
            raise ValueError("Conversation not found")

        # Get conversation history
        history = await self._get_conversation_history(conversation_id)

        # Detect intent
        intent = await self._classify_intent(content, code_snippet)

        # Enforce guardrails BEFORE sending to AI (FR-027, FR-028)
        guardrail_violation = enforce_guardrails(
            content, intent, history, understanding_level
        )

        if guardrail_violation:
            # Guardrail triggered - use suggested response
            return await self._handle_guardrail_violation(
                conversation, content, guardrail_violation, intent
            )

        # Get stage level for agent adaptation
        stage_level = await self._get_stage_level(conversation.stage_id) if conversation.stage_id else 3

        # Create appropriate agent
        agent = create_tutor_agent(stage_level)

        # Run agent conversation
        try:
            result = await run_tutor_conversation(
                agent,
                content,
                session_id=str(conversation_id),
                db_path="data/tutor_sessions.db"
            )

            ai_response = result["final_output"]

            # Validate AI response doesn't violate guardrails (FR-028)
            response_violation = validate_ai_response(ai_response, intent)
            if response_violation:
                # AI tried to give solution - use hints instead
                ai_response = response_violation.suggested_response

                # Log the guardrail event
                await self._log_guardrail_event(
                    conversation_id,
                    None,
                    response_violation.guardrail_type,
                    response_violation.reason,
                    content,
                    ai_response,
                )

            # Store user message
            user_msg = await self._store_message(
                conversation_id,
                "user",
                content,
                code_snippet=code_snippet,
                detected_intent=intent,
                understanding_level=understanding_level,
            )

            # Store assistant message
            response_time_ms = int((datetime.utcnow() - start_time).total_seconds() * 1000)
            assistant_msg = await self._store_message(
                conversation_id,
                "assistant",
                ai_response,
                response_type="socratic_guidance",
                response_time_ms=response_time_ms,
            )

            # Update conversation
            conversation.intent_type = intent
            conversation.updated_at = datetime.utcnow()
            await self.db.commit()

            # Check if escalation needed (FR-035)
            should_escalate, escalation_reason = await self._check_escalation_needed(
                conversation_id, understanding_level
            )

            return TutorResponseDTO(
                message_id=assistant_msg.id,
                conversation_id=conversation_id,
                content=ai_response,
                response_type="socratic_guidance",
                guardrail_triggered=False,
                adapted_for_level=stage_level,
                escalation_available=should_escalate,
                escalation_reason=escalation_reason,
            )

        except Exception as e:
            # Log error and provide fallback
            print(f"AI Tutor error: {e}")
            return await self._fallback_response(conversation, content, intent)

    async def request_debugging_help(
        self,
        conversation_id: uuid.UUID,
        user_id: uuid.UUID,
        code: str,
        error_message: Optional[str],
        expected_behavior: str,
        actual_behavior: str,
    ) -> DebuggingGuidanceDTO:
        """
        Provide systematic debugging guidance (FR-030)
        """
        conversation = await self.get_conversation(conversation_id, user_id)
        if not conversation:
            raise ValueError("Conversation not found")

        # Use debugging agent tool
        stage_level = await self._get_stage_level(conversation.stage_id) if conversation.stage_id else 3
        agent = create_tutor_agent(stage_level)

        # In production, call the provide_debugging_guidance tool
        # For now, return structured guidance
        guidance = DebuggingGuidanceDTO(
            message_id=uuid.uuid4(),
            conversation_id=conversation_id,
            observation=f"Expected: {expected_behavior}, Actual: {actual_behavior}",
            hypothesis=[
                "Variable initialization issue",
                "Logic error in conditionals",
                "Data type mismatch",
            ],
            verification_steps=[
                {
                    "step": "1. Check variable values",
                    "action": "Add print statements before and after key operations",
                    "expected_result": "See where values diverge from expected"
                },
                {
                    "step": "2. Test with simple input",
                    "action": "Use minimal test case",
                    "expected_result": "Isolate the failing component"
                },
            ],
            hints=[
                "Start by verifying your assumptions about the data",
                "Use a debugger or print statements to trace execution",
            ],
            guiding_questions=[
                "What assumptions are you making?",
                "What happens if you trace through step by step?",
                "Where does actual behavior first deviate?",
            ],
        )

        return guidance

    async def request_code_review(
        self,
        conversation_id: uuid.UUID,
        user_id: uuid.UUID,
        code: str,
        language: str,
        context: str,
    ) -> CodeReviewDTO:
        """
        Provide code review without solutions (FR-031)
        """
        conversation = await self.get_conversation(conversation_id, user_id)
        if not conversation:
            raise ValueError("Conversation not found")

        # Placeholder - in production, use agent's code review tool
        review = CodeReviewDTO(
            message_id=uuid.uuid4(),
            conversation_id=conversation_id,
            issues=[
                {
                    "line": "5",
                    "severity": "medium",
                    "category": "logic",
                    "description": "Potential edge case not handled",
                    "hint": "What happens with empty input?"
                }
            ],
            strengths=["Clear variable names", "Good structure"],
            improvement_questions=[
                "How would you handle errors?",
                "Could this be more efficient?",
            ],
            concepts_to_review=["Error handling", "Edge cases"],
            best_practices=["Add input validation", "Include unit tests"],
            solution_provided=False,
        )

        return review

    async def escalate_to_instructor(
        self,
        conversation_id: uuid.UUID,
        user_id: uuid.UUID,
        reason: str,
    ) -> EscalationResponse:
        """
        Escalate conversation to human instructor (FR-035)
        """
        conversation = await self.get_conversation(conversation_id, user_id)
        if not conversation:
            raise ValueError("Conversation not found")

        # Log escalation event
        event = GuardrailEvent(
            conversation_id=conversation_id,
            guardrail_type=GuardrailType.ESCALATION_TRIGGERED,
            trigger_reason=reason,
            escalated=True,
            escalation_reason=reason,
            severity="high",
            action_taken="Notified instructor",
        )
        self.db.add(event)
        await self.db.commit()

        # In production: send notification to instructor
        # For now, return confirmation
        reference_number = f"ESC-{conversation_id.hex[:8].upper()}"

        return EscalationResponse(
            conversation_id=conversation_id,
            escalated_at=datetime.utcnow(),
            instructor_notified=True,
            estimated_response_time="Within 24 hours",
            reference_number=reference_number,
        )

    # Helper methods
    async def _classify_intent(self, message: str, code: Optional[str]) -> IntentType:
        """Classify user intent"""
        message_lower = message.lower()

        if code:
            if "error" in message_lower or "bug" in message_lower:
                return IntentType.DEBUG
            elif "review" in message_lower:
                return IntentType.CODE_REVIEW
            else:
                return IntentType.CODE
        elif any(word in message_lower for word in ["explain", "what is", "why"]):
            return IntentType.CONCEPT
        elif any(word in message_lower for word in ["give me", "show me", "tell me the answer"]):
            return IntentType.DIRECT_ANSWER
        else:
            return IntentType.EXPLANATION

    async def _get_conversation_history(self, conversation_id: uuid.UUID) -> List[Dict]:
        """Get conversation history for context"""
        query = (
            select(AIMessage)
            .where(AIMessage.conversation_id == conversation_id)
            .order_by(AIMessage.created_at)
        )
        result = await self.db.execute(query)
        messages = result.scalars().all()

        return [{"role": msg.role, "content": msg.content} for msg in messages]

    async def _get_stage_level(self, stage_id: uuid.UUID) -> int:
        """Get stage level for agent adaptation"""
        query = select(Stage).where(Stage.id == stage_id)
        result = await self.db.execute(query)
        stage = result.scalar_one_or_none()
        return stage.level if stage and hasattr(stage, "level") else 3

    async def _store_message(
        self,
        conversation_id: uuid.UUID,
        role: str,
        content: str,
        **kwargs,
    ) -> AIMessage:
        """Store message in database"""
        message = AIMessage(
            conversation_id=conversation_id,
            role=role,
            content=content,
            **kwargs,
        )
        self.db.add(message)
        await self.db.commit()
        await self.db.refresh(message)
        return message

    async def _log_guardrail_event(
        self,
        conversation_id: uuid.UUID,
        message_id: Optional[uuid.UUID],
        guardrail_type: GuardrailType,
        reason: str,
        original_request: str,
        modified_response: str,
    ):
        """Log guardrail trigger"""
        event = GuardrailEvent(
            conversation_id=conversation_id,
            message_id=message_id,
            guardrail_type=guardrail_type,
            trigger_reason=reason,
            original_request=original_request,
            modified_response=modified_response,
            severity="medium",
            action_taken="Redirected to Socratic response",
        )
        self.db.add(event)
        await self.db.commit()

    async def _handle_guardrail_violation(
        self,
        conversation: AIConversation,
        user_message: str,
        violation: GuardrailViolation,
        intent: IntentType,
    ) -> TutorResponseDTO:
        """Handle guardrail violation"""
        # Store messages
        user_msg = await self._store_message(
            conversation.id,
            "user",
            user_message,
            detected_intent=intent,
        )

        assistant_msg = await self._store_message(
            conversation.id,
            "assistant",
            violation.suggested_response,
            response_type="guardrail_redirect",
        )

        # Log guardrail event
        await self._log_guardrail_event(
            conversation.id,
            assistant_msg.id,
            violation.guardrail_type,
            violation.reason,
            user_message,
            violation.suggested_response,
        )

        return TutorResponseDTO(
            message_id=assistant_msg.id,
            conversation_id=conversation.id,
            content=violation.suggested_response,
            response_type="guardrail_redirect",
            guardrail_triggered=True,
            guardrail_message=violation.reason,
        )

    async def _check_escalation_needed(
        self, conversation_id: uuid.UUID, understanding_level: Optional[int]
    ) -> Tuple[bool, Optional[str]]:
        """Check if escalation to instructor is recommended"""
        history = await self._get_conversation_history(conversation_id)

        # Check conversation length and understanding
        if len(history) > 6 and understanding_level and understanding_level < 2:
            return True, "Student needs additional support after multiple attempts"

        return False, None

    async def _fallback_response(
        self, conversation: AIConversation, user_message: str, intent: IntentType
    ) -> TutorResponseDTO:
        """Fallback response if agent fails"""
        fallback_content = (
            "I'm having trouble processing that right now. "
            "Let me ask you some questions to better understand:\n\n"
            "1. What are you trying to accomplish?\n"
            "2. What have you tried so far?\n"
            "3. What specific part is confusing?"
        )

        msg = await self._store_message(
            conversation.id,
            "assistant",
            fallback_content,
            response_type="fallback",
        )

        return TutorResponseDTO(
            message_id=msg.id,
            conversation_id=conversation.id,
            content=fallback_content,
            response_type="fallback",
        )
