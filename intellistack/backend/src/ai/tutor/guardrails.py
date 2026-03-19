"""
AI Tutor Guardrails System
FR-027: Socratic method enforcement
FR-028: Refuse direct code solutions
FR-035: Escalation logic
"""

import re
from typing import Dict, List, Tuple, Optional
from enum import Enum

from .models import GuardrailType, IntentType


class GuardrailViolation(Exception):
    """Exception raised when a guardrail is violated"""

    def __init__(self, guardrail_type: GuardrailType, reason: str, suggested_response: str):
        self.guardrail_type = guardrail_type
        self.reason = reason
        self.suggested_response = suggested_response
        super().__init__(reason)


class SocraticGuardrails:
    """
    Enforces Socratic teaching methodology
    FR-027: Guide learning through questions, not direct answers
    """

    # Patterns that indicate direct answer requests
    DIRECT_ANSWER_PATTERNS = [
        r"give\s+me\s+the\s+(answer|solution|code)",
        r"what\s+is\s+the\s+(answer|solution|code)",
        r"(tell|show)\s+me\s+(the\s+)?(answer|solution|code)",
        r"just\s+(give|show|tell)\s+me",
        r"what\s+should\s+i\s+write",
        r"write\s+the\s+code\s+for",
        r"solve\s+this\s+for\s+me",
        r"do\s+this\s+for\s+me",
        r"complete\s+this\s+code",
    ]

    # Socratic question templates
    SOCRATIC_QUESTIONS = {
        "clarification": [
            "What exactly are you trying to accomplish?",
            "Can you explain what you understand so far?",
            "What have you tried already?",
        ],
        "decomposition": [
            "What are the smaller steps needed to solve this?",
            "Can you break this problem into parts?",
            "What would you solve first if you had to start somewhere?",
        ],
        "reasoning": [
            "Why do you think that approach would work?",
            "What happens if you try that?",
            "How does this relate to concepts you've learned?",
        ],
        "exploration": [
            "What would happen if you changed X?",
            "Have you seen a similar problem before?",
            "What resources could help you figure this out?",
        ],
        "metacognition": [
            "What's making this challenging for you?",
            "What do you need to understand better?",
            "How would you explain this to someone else?",
        ],
    }

    @classmethod
    def check_direct_answer_request(cls, user_message: str) -> Tuple[bool, Optional[str]]:
        """
        Detect if user is requesting a direct answer
        Returns: (is_violation, reason)
        """
        message_lower = user_message.lower()

        for pattern in cls.DIRECT_ANSWER_PATTERNS:
            if re.search(pattern, message_lower):
                return True, f"Direct answer request detected: '{user_message[:50]}...'"

        return False, None

    @classmethod
    def generate_redirect_response(cls, intent: IntentType, original_request: str) -> str:
        """
        Generate a Socratic redirect instead of direct answer
        FR-027: Guide learning through questions
        """
        base_message = (
            "I'm here to help you learn, not just give answers! 🤔\n\n"
            "Instead of telling you the solution, let me guide you:\n\n"
        )

        if intent == IntentType.CODE:
            questions = [
                "1. What are you trying to accomplish with this code?",
                "2. What approaches have you considered?",
                "3. What's the first step you could take?",
            ]
        elif intent == IntentType.DEBUG:
            questions = [
                "1. What error or unexpected behavior are you seeing?",
                "2. What did you expect to happen?",
                "3. What have you checked so far?",
            ]
        elif intent == IntentType.CONCEPT:
            questions = [
                "1. What do you already understand about this concept?",
                "2. Can you think of an example or analogy?",
                "3. What specific part is confusing?",
            ]
        else:
            questions = cls.SOCRATIC_QUESTIONS["clarification"]

        return base_message + "\n".join(questions) + "\n\n💡 Answer these, and we'll work through it together!"

    @classmethod
    def generate_guiding_questions(cls, category: str, context: Optional[str] = None) -> List[str]:
        """
        Generate contextual guiding questions
        """
        questions = cls.SOCRATIC_QUESTIONS.get(category, cls.SOCRATIC_QUESTIONS["reasoning"])
        return questions[:3]  # Return top 3 relevant questions


class CodeSolutionGuardrails:
    """
    Prevents direct code solutions
    FR-028: AI refuses to provide complete solutions
    """

    # Code block patterns
    CODE_BLOCK_PATTERN = r"```[\w]*\n(.*?)\n```"

    # Patterns indicating full solutions
    SOLUTION_INDICATORS = [
        r"here\s+is\s+the\s+(complete|full)\s+code",
        r"here's\s+your\s+solution",
        r"copy\s+this\s+code",
        r"use\s+this\s+code",
        r"this\s+will\s+work",
    ]

    @classmethod
    def check_response_for_solution(cls, response: str) -> Tuple[bool, Optional[str]]:
        """
        Check if AI response contains a complete solution
        Returns: (is_violation, reason)
        """
        response_lower = response.lower()

        # Check for solution indicators
        for pattern in cls.SOLUTION_INDICATORS:
            if re.search(pattern, response_lower):
                return True, "Response contains solution indicator phrases"

        # Check code blocks
        code_blocks = re.findall(cls.CODE_BLOCK_PATTERN, response, re.DOTALL)

        if code_blocks:
            # Check if code is too complete (heuristic)
            for code in code_blocks:
                lines = [l.strip() for l in code.split("\n") if l.strip() and not l.strip().startswith("#")]

                # If code block has >10 lines of actual code, it might be a full solution
                if len(lines) > 10:
                    return True, f"Code block with {len(lines)} lines detected - may be full solution"

        return False, None

    @classmethod
    def convert_to_hints(cls, code_explanation: str) -> Dict[str, any]:
        """
        Convert code explanation to hints instead of solutions
        """
        return {
            "hints": [
                "Think about the structure you need",
                "Consider what data types would work",
                "Break the problem into smaller functions",
            ],
            "guiding_questions": [
                "What's the main goal of this function?",
                "What inputs and outputs do you need?",
                "What edge cases should you handle?",
            ],
            "concepts_to_review": [
                "Function parameters and return values",
                "Data structures for this problem",
                "Error handling best practices",
            ],
        }


class EscalationGuardrails:
    """
    Determines when to escalate to human instructor
    FR-035: Escalate when AI cannot help effectively
    """

    # Reasons to escalate
    ESCALATION_TRIGGERS = {
        "repeated_confusion": "Student still confused after 3+ attempts",
        "complex_debugging": "Debugging issue beyond systematic approach",
        "misconception": "Deep conceptual misconception detected",
        "safety_concern": "Code involves safety-critical systems",
        "out_of_scope": "Question outside course curriculum",
        "student_request": "Student explicitly requests human help",
    }

    @classmethod
    def should_escalate(
        cls,
        conversation_history: List[Dict],
        current_intent: IntentType,
        understanding_level: Optional[int],
    ) -> Tuple[bool, Optional[str]]:
        """
        Determine if conversation should be escalated to instructor
        """
        # Check conversation length (repeated confusion)
        if len(conversation_history) > 6:
            # Check if student understanding hasn't improved
            if understanding_level and understanding_level < 2:
                return True, cls.ESCALATION_TRIGGERS["repeated_confusion"]

        # Check for explicit escalation requests
        if conversation_history:
            last_message = conversation_history[-1].get("content", "").lower()
            escalation_keywords = ["talk to instructor", "human help", "teacher", "professor"]
            if any(keyword in last_message for keyword in escalation_keywords):
                return True, cls.ESCALATION_TRIGGERS["student_request"]

        return False, None

    @classmethod
    def generate_escalation_message(cls, reason: str) -> str:
        """Generate friendly escalation message"""
        return (
            f"I think it would be helpful to connect you with an instructor for this.\n\n"
            f"**Reason:** {reason}\n\n"
            f"Would you like me to escalate this to your instructor? "
            f"They can provide more personalized guidance for your situation.\n\n"
            f"Reply 'yes' to escalate, or 'no' to continue working together."
        )


class UnderstandingVerificationGuardrails:
    """
    Verifies student understanding before proceeding
    FR-046: Understanding Verification Framework
    """

    VERIFICATION_QUESTIONS = {
        1: [  # Low understanding
            "Can you explain this in your own words?",
            "What's one thing you understand about this?",
            "What's confusing you the most?",
        ],
        2: [  # Basic understanding
            "Can you give an example of when you'd use this?",
            "What would happen if you changed X?",
            "How does this relate to Y?",
        ],
        3: [  # Moderate understanding
            "Can you explain why this approach works?",
            "What are the trade-offs here?",
            "How would you optimize this?",
        ],
        4: [  # Good understanding
            "Can you think of an edge case?",
            "How would you explain this to a beginner?",
            "What alternatives exist?",
        ],
        5: [  # Strong understanding
            "Can you extend this concept?",
            "What are the limitations?",
            "How does this fit into the bigger picture?",
        ],
    }

    @classmethod
    def get_verification_questions(cls, understanding_level: int) -> List[str]:
        """Get appropriate verification questions based on level"""
        return cls.VERIFICATION_QUESTIONS.get(understanding_level, cls.VERIFICATION_QUESTIONS[3])

    @classmethod
    def should_verify_before_proceeding(cls, conversation_history: List[Dict]) -> bool:
        """
        Check if we should verify understanding before moving forward
        """
        # Verify every 3 exchanges
        return len(conversation_history) % 6 == 0 and len(conversation_history) > 0


def enforce_guardrails(
    user_message: str,
    intent: IntentType,
    conversation_history: List[Dict],
    understanding_level: Optional[int] = None,
) -> Optional[GuardrailViolation]:
    """
    Main guardrail enforcement function
    Checks all guardrails and raises violation if needed

    Returns None if all guardrails pass, or GuardrailViolation if violated
    """

    # Check for direct answer requests (FR-027)
    is_direct, reason = SocraticGuardrails.check_direct_answer_request(user_message)
    if is_direct:
        redirect = SocraticGuardrails.generate_redirect_response(intent, user_message)
        return GuardrailViolation(
            guardrail_type=GuardrailType.SOCRATIC_REDIRECT,
            reason=reason,
            suggested_response=redirect,
        )

    # Check for escalation need (FR-035)
    should_escalate, escalation_reason = EscalationGuardrails.should_escalate(
        conversation_history, intent, understanding_level
    )
    if should_escalate:
        escalation_msg = EscalationGuardrails.generate_escalation_message(escalation_reason)
        return GuardrailViolation(
            guardrail_type=GuardrailType.ESCALATION_TRIGGERED,
            reason=escalation_reason,
            suggested_response=escalation_msg,
        )

    # No violations
    return None


def validate_ai_response(response: str, intent: IntentType) -> Optional[GuardrailViolation]:
    """
    Validate AI-generated response against guardrails
    Prevents the AI from accidentally providing full solutions

    Returns None if response is acceptable, or GuardrailViolation if it needs modification
    """

    # Check for code solutions (FR-028)
    if intent in [IntentType.CODE, IntentType.DEBUG, IntentType.CODE_REVIEW]:
        is_solution, reason = CodeSolutionGuardrails.check_response_for_solution(response)
        if is_solution:
            hints = CodeSolutionGuardrails.convert_to_hints(response)
            return GuardrailViolation(
                guardrail_type=GuardrailType.CODE_SOLUTION_BLOCKED,
                reason=reason,
                suggested_response=f"I can't provide the full solution, but here are some hints:\n\n{hints}",
            )

    # No violations
    return None
