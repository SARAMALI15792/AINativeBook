"""
AI Tutor API Routes
FR-026 to FR-035: Socratic AI Tutor Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import uuid

from ...shared.database import get_session as get_db
from ...core.auth.dependencies import get_current_user
from .service import AITutorService
from .schemas import (
    CreateTutorConversationRequest,
    SendTutorMessageRequest,
    CodeReviewRequest,
    DebuggingHelpRequest,
    EscalateToInstructorRequest,
    AIConversationResponse,
    TutorResponseDTO,
    DebuggingGuidanceDTO,
    CodeReviewDTO,
    EscalationResponse,
)

router = APIRouter(prefix="/ai/tutor", tags=["AI Tutor"])


@router.post("/conversations", response_model=AIConversationResponse, status_code=status.HTTP_201_CREATED)
async def create_tutor_conversation(
    request: CreateTutorConversationRequest,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Create a new AI tutor conversation (FR-026)

    Students can start conversations for:
    - Conceptual questions
    - Code help
    - Debugging assistance
    - Code review
    """
    service = AITutorService(db)

    conversation = await service.create_conversation(
        user_id=current_user.id,
        stage_id=request.stage_id,
        content_id=request.content_id,
        initial_message=request.initial_message,
    )

    # Send first message to get initial response
    if request.initial_message:
        await service.send_message(
            conversation_id=conversation.id,
            user_id=current_user.id,
            content=request.initial_message,
            code_snippet=request.code_snippet,
        )

        # Refresh to get messages
        conversation = await service.get_conversation(conversation.id, current_user.id)

    return conversation


@router.get("/conversations/{conversation_id}", response_model=AIConversationResponse)
async def get_tutor_conversation(
    conversation_id: uuid.UUID,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Get conversation history (FR-034)
    """
    service = AITutorService(db)
    conversation = await service.get_conversation(conversation_id, current_user.id)

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    return conversation


@router.post("/conversations/{conversation_id}/messages", response_model=TutorResponseDTO)
async def send_tutor_message(
    conversation_id: uuid.UUID,
    request: SendTutorMessageRequest,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Send message to AI tutor and receive Socratic guidance (FR-027, FR-028)

    The AI tutor will:
    - Guide learning through questions (Socratic method)
    - Refuse to provide direct solutions
    - Adapt responses to student understanding level
    - Enforce guardrails to prevent solution-giving
    """
    service = AITutorService(db)

    try:
        response = await service.send_message(
            conversation_id=conversation_id,
            user_id=current_user.id,
            content=request.content,
            code_snippet=request.code_snippet,
            understanding_level=request.understanding_level,
        )
        return response

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/debugging-help", response_model=DebuggingGuidanceDTO)
async def request_debugging_help(
    request: DebuggingHelpRequest,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Get systematic debugging guidance (FR-030)

    Provides step-by-step debugging methodology:
    - Observation → Hypothesis → Verification
    - Guiding questions to lead to discovery
    - Hints without direct solutions
    """
    service = AITutorService(db)

    # Create or use existing conversation
    if request.conversation_id:
        conversation_id = request.conversation_id
    else:
        conversation = await service.create_conversation(
            user_id=current_user.id,
            stage_id=request.stage_id,
            initial_message=f"Debugging help: {request.expected_behavior}",
        )
        conversation_id = conversation.id

    try:
        guidance = await service.request_debugging_help(
            conversation_id=conversation_id,
            user_id=current_user.id,
            code=request.code,
            error_message=request.error_message,
            expected_behavior=request.expected_behavior,
            actual_behavior=request.actual_behavior,
        )
        return guidance

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/code-review", response_model=CodeReviewDTO)
async def request_code_review(
    request: CodeReviewRequest,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Get code review without solutions (FR-031)

    Provides:
    - Identification of issues with hints
    - Guiding questions for improvement
    - Best practices to apply
    - NO direct code fixes or solutions
    """
    service = AITutorService(db)

    # Create or use existing conversation
    if request.conversation_id:
        conversation_id = request.conversation_id
    else:
        conversation = await service.create_conversation(
            user_id=current_user.id,
            stage_id=request.stage_id,
            initial_message=f"Code review: {request.context}",
        )
        conversation_id = conversation.id

    try:
        review = await service.request_code_review(
            conversation_id=conversation_id,
            user_id=current_user.id,
            code=request.code,
            language=request.language,
            context=request.context,
        )
        return review

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/conversations/{conversation_id}/escalate", response_model=EscalationResponse)
async def escalate_to_instructor(
    conversation_id: uuid.UUID,
    request: EscalateToInstructorRequest,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Escalate conversation to human instructor (FR-035)

    Escalation triggers:
    - Student stuck after multiple attempts
    - Complex issues beyond AI's scope
    - Student explicit request
    - Safety-critical code
    """
    service = AITutorService(db)

    try:
        response = await service.escalate_to_instructor(
            conversation_id=conversation_id,
            user_id=current_user.id,
            reason=request.reason,
        )
        return response

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "ai_tutor"}
