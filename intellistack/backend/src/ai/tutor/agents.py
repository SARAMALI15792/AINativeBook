"""
AI Tutor Agents using OpenAI Agents SDK
FR-026 to FR-035: Socratic AI Tutor Implementation
Latest patterns from Context7: OpenAI Agents Python SDK
"""

import asyncio
from typing import Annotated, List, Dict, Optional, Any
from pydantic import BaseModel, Field
from enum import Enum

from agents import Agent, Runner, SQLiteSession, function_tool

from .models import IntentType
from .guardrails import (
    SocraticGuardrails,
    CodeSolutionGuardrails,
    UnderstandingVerificationGuardrails,
)


# ============================================================================
# Pydantic Models for Function Tool Returns
# ============================================================================

class IntentClassification(BaseModel):
    """Intent classification result"""
    intent: IntentType = Field(description="Detected intent type")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence score")
    reasoning: str = Field(description="Why this intent was chosen")
    understanding_level: Optional[int] = Field(None, ge=1, le=5, description="Estimated understanding level")


class SocraticResponse(BaseModel):
    """Socratic teaching response structure"""
    guiding_questions: List[str] = Field(description="Questions to guide thinking")
    hints: List[str] = Field(default_factory=list, description="Subtle hints without solutions")
    concepts_to_review: List[str] = Field(default_factory=list, description="Concepts student should review")
    next_steps: List[str] = Field(description="Suggested next steps for learning")


class DebuggingGuidance(BaseModel):
    """Systematic debugging guidance (FR-030)"""
    observation: str = Field(description="What we observe from the error/behavior")
    hypotheses: List[str] = Field(description="Possible causes to investigate")
    verification_steps: List[Dict[str, str]] = Field(description="Systematic steps to verify hypotheses")
    guiding_questions: List[str] = Field(description="Questions to help student think through the problem")
    hints: List[str] = Field(default_factory=list, description="Hints for debugging")


class CodeReviewFeedback(BaseModel):
    """Code review without solutions (FR-031)"""
    strengths: List[str] = Field(description="Positive aspects of the code")
    issues: List[Dict[str, str]] = Field(description="Issues found with line, type, description, hint")
    improvement_questions: List[str] = Field(description="Questions for improvement")
    concepts_to_review: List[str] = Field(description="Concepts to study")
    best_practices: List[str] = Field(description="Best practices to apply")


# ============================================================================
# Function Tools for AI Tutor Agent
# ============================================================================

@function_tool
async def classify_intent(
    user_message: Annotated[str, "The student's message to classify"],
    conversation_context: Annotated[str, "Summary of previous conversation"] = "",
) -> IntentClassification:
    """
    Classify the student's intent to determine appropriate teaching approach.

    Categories:
    - concept: Asking about theoretical concepts
    - code: Requesting help writing code
    - debug: Debugging existing code
    - direct_answer: Requesting direct solutions (will be redirected)
    - code_review: Requesting code review
    - explanation: Asking for explanations

    Args:
        user_message: The student's current message
        conversation_context: Summary of previous messages for context
    """
    # This is a placeholder - in production, use lightweight classification
    # For now, use simple keyword detection
    message_lower = user_message.lower()

    if any(word in message_lower for word in ["explain", "what is", "why does", "how does"]):
        return IntentClassification(
            intent=IntentType.CONCEPT,
            confidence=0.8,
            reasoning="Student is asking conceptual questions",
            understanding_level=3
        )
    elif any(word in message_lower for word in ["error", "bug", "not working", "issue", "problem"]):
        return IntentClassification(
            intent=IntentType.DEBUG,
            confidence=0.85,
            reasoning="Student has debugging needs",
            understanding_level=2
        )
    elif any(word in message_lower for word in ["review my code", "check my code", "feedback on"]):
        return IntentClassification(
            intent=IntentType.CODE_REVIEW,
            confidence=0.9,
            reasoning="Student wants code review",
            understanding_level=3
        )
    elif any(word in message_lower for word in ["give me", "show me", "tell me the answer", "solve this"]):
        return IntentClassification(
            intent=IntentType.DIRECT_ANSWER,
            confidence=0.95,
            reasoning="Student requesting direct answer",
            understanding_level=1
        )
    else:
        return IntentClassification(
            intent=IntentType.CODE,
            confidence=0.7,
            reasoning="General code-related question",
            understanding_level=3
        )


@function_tool
async def generate_socratic_response(
    student_question: Annotated[str, "The student's question"],
    understanding_level: Annotated[int, "Student's understanding level (1-5)"],
    topic: Annotated[str, "The topic being discussed"],
) -> SocraticResponse:
    """
    Generate Socratic teaching response (FR-027).

    Instead of providing direct answers, guide learning through questions.
    Adapt complexity based on understanding level.

    Args:
        student_question: What the student asked
        understanding_level: Estimated understanding (1=beginner, 5=advanced)
        topic: Current topic/concept
    """
    # Generate appropriate guiding questions based on level
    questions = SocraticGuardrails.generate_guiding_questions("reasoning", student_question)

    return SocraticResponse(
        guiding_questions=questions,
        hints=[
            "Think about what you already know about this topic",
            "Consider breaking the problem into smaller parts",
            "What examples have you seen that are similar?",
        ][:understanding_level],  # More hints for lower levels
        concepts_to_review=[topic],
        next_steps=[
            "Answer the guiding questions above",
            "Try to work through an example",
            "Share your thinking process with me",
        ]
    )


@function_tool
async def provide_debugging_guidance(
    code: Annotated[str, "The code with the issue"],
    error_message: Annotated[str, "Error message or description of unexpected behavior"],
    expected_behavior: Annotated[str, "What should happen"],
    actual_behavior: Annotated[str, "What actually happens"],
) -> DebuggingGuidance:
    """
    Provide systematic debugging methodology (FR-030).

    Guide students through debugging process without fixing the code for them.
    Teach systematic problem-solving approach.

    Args:
        code: The problematic code
        error_message: Error or issue description
        expected_behavior: Expected outcome
        actual_behavior: Actual outcome
    """
    return DebuggingGuidance(
        observation=f"The code produces '{actual_behavior}' instead of '{expected_behavior}'",
        hypotheses=[
            "Check variable initialization and data types",
            "Verify function parameters and return values",
            "Look for off-by-one errors or boundary conditions",
            "Consider the order of operations",
        ],
        verification_steps=[
            {
                "step": "1. Add print statements",
                "action": "Print variable values at key points",
                "expected_result": "See where values deviate from expected"
            },
            {
                "step": "2. Check assumptions",
                "action": "Verify data types and ranges",
                "expected_result": "Confirm inputs match expectations"
            },
            {
                "step": "3. Simplify the problem",
                "action": "Test with minimal input",
                "expected_result": "Isolate the failing component"
            },
        ],
        guiding_questions=[
            "What assumptions are you making about the data?",
            "What happens if you trace through the code step by step?",
            "Where does the actual behavior first deviate from expected?",
            "What would happen if you tested with simpler input?",
        ],
        hints=[
            "Start by verifying your input data",
            "Use print debugging or a debugger to track execution",
            "Test edge cases separately",
        ]
    )


@function_tool
async def provide_code_review(
    code: Annotated[str, "The code to review"],
    language: Annotated[str, "Programming language"],
    context: Annotated[str, "What the code is supposed to do"],
) -> CodeReviewFeedback:
    """
    Provide code review without auto-fix (FR-031).

    Highlight issues and provide hints, but never provide corrected code.
    Guide students to improve their own code.

    Args:
        code: Code to review
        language: Programming language
        context: Purpose of the code
    """
    # Placeholder - in production, analyze code structure
    return CodeReviewFeedback(
        strengths=[
            "Code structure is clear and readable",
            "Variable names are descriptive",
        ],
        issues=[
            {
                "line": "5",
                "type": "logic",
                "description": "This condition might not handle edge cases",
                "hint": "What happens when the input is empty?"
            },
            {
                "line": "10",
                "type": "style",
                "description": "Consider extracting this into a helper function",
                "hint": "Think about code reusability"
            },
        ],
        improvement_questions=[
            "How would you handle invalid input?",
            "Could this be more efficient?",
            "What would happen with very large inputs?",
        ],
        concepts_to_review=[
            "Error handling best practices",
            "Code modularity and functions",
        ],
        best_practices=[
            "Add input validation",
            "Include error handling",
            "Write unit tests for edge cases",
        ]
    )


# ============================================================================
# AI Tutor Agent Configuration
# ============================================================================

def create_tutor_agent(stage_level: int = 1) -> Agent:
    """
    Create AI Tutor agent with Socratic teaching approach (FR-026 to FR-035)

    Args:
        stage_level: Learning stage (1-5) to adapt instruction complexity

    Returns:
        Configured Agent instance
    """

    # Adapt instructions based on stage
    stage_instructions = {
        1: "You're helping a beginner student. Use simple language and basic concepts.",
        2: "You're helping a student learning ROS 2 and robotics. Build on fundamentals.",
        3: "You're helping a student learning computer vision. Assume basic robotics knowledge.",
        4: "You're helping a student learning AI/ML for robotics. Assume CV knowledge.",
        5: "You're helping an advanced student on their capstone. Challenge them appropriately.",
    }

    instructions = f"""You are a Socratic AI Tutor for robotics and humanoid robotics learning.

**Core Principle (FR-027):** Guide learning through questions, NOT direct answers.

**Your Teaching Approach:**
1. **Ask guiding questions** instead of providing solutions
2. **Provide hints**, not complete answers
3. **Encourage systematic thinking** and problem-solving
4. **Verify understanding** before advancing concepts
5. **Adapt to student level**: {stage_instructions.get(stage_level, stage_instructions[3])}

**Critical Rules (FR-028):**
- NEVER provide complete code solutions
- NEVER directly solve problems for students
- NEVER give answers that bypass learning
- ALWAYS redirect direct answer requests to guiding questions

**For Debugging (FR-030):**
- Teach systematic debugging methodology
- Guide through observation → hypothesis → verification
- Ask questions that lead to discovery, not answers

**For Code Review (FR-031):**
- Point out issues with hints, not fixes
- Ask improvement questions
- Suggest concepts to review, not code changes

**Understanding Verification (FR-046):**
- Regularly check student understanding
- Ask them to explain concepts in their own words
- Adjust complexity based on their responses

**When to Escalate (FR-035):**
- Student stuck after 3+ attempts
- Deep misconceptions detected
- Safety-critical code involved
- Student explicitly requests human help

Remember: Your goal is to make students think, not to make their work easier!
"""

    agent = Agent(
        name="SocraticTutor",
        instructions=instructions,
        tools=[
            classify_intent,
            generate_socratic_response,
            provide_debugging_guidance,
            provide_code_review,
        ],
        model="gpt-4o",  # Using GPT-4 for better reasoning
    )

    return agent


async def run_tutor_conversation(
    agent: Agent,
    user_message: str,
    session_id: str,
    db_path: str = "tutor_conversations.db",
) -> Dict[str, Any]:
    """
    Run a single turn of tutor conversation with session persistence

    Args:
        agent: The tutor agent
        user_message: Student's message
        session_id: Unique conversation ID
        db_path: SQLite database path for session storage

    Returns:
        Result dictionary with final_output and metadata
    """
    # Create persistent session (FR-033, FR-034)
    session = SQLiteSession(session_id, db_path)

    # Run agent with conversation context
    result = await Runner.run(
        agent,
        user_message,
        session=session
    )

    return {
        "final_output": result.final_output,
        "session_id": session_id,
        "turns": len(await session.get_items()) // 2,  # User + Assistant = 1 turn
    }


# ============================================================================
# Synchronous Wrapper for FastAPI
# ============================================================================

def run_tutor_sync(
    agent: Agent,
    user_message: str,
    session_id: str,
    db_path: str = "tutor_conversations.db",
) -> Dict[str, Any]:
    """
    Synchronous wrapper for FastAPI routes
    """
    return asyncio.run(run_tutor_conversation(agent, user_message, session_id, db_path))
