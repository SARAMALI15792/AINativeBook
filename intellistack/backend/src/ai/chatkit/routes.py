"""
ChatKit API Routes

FastAPI routes for ChatKit protocol handling.
Provides SSE streaming for AI responses.
"""

import json
import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.database import get_session as get_db
from src.core.auth.dependencies import (
    get_current_user,
    AuthenticatedUser,
)
from src.ai.rag.config import get_qdrant_config
from src.ai.rag.vector_store import VectorStore
from src.ai.rag.retrieval import HybridRetriever
from .server import IntelliStackChatKitServer
from .context import RequestContext, PageContext

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/chatkit", tags=["chatkit"])


# Retriever dependency for RAG integration
_retriever_instance = None


def get_retriever() -> HybridRetriever:
    """
    Get or create RAG retriever for ChatKit integration.

    This enables the ChatKit AI tutor to use the full RAG pipeline
    with Qdrant vector search and Cohere reranking.
    """
    global _retriever_instance

    if _retriever_instance is None:
        try:
            from src.ai.shared.llm_client import LLMClient
            config = get_qdrant_config()
            llm_client = LLMClient()
            vector_store = VectorStore(config)
            _retriever_instance = HybridRetriever(
                vector_store=vector_store,
                llm_client=llm_client,
                config=config,
            )
            logger.info("ChatKit RAG retriever initialized")
        except Exception as e:
            logger.warning(f"Failed to initialize RAG retriever for ChatKit: {e}")
            return None

    return _retriever_instance


# Request/Response Models
class CreateThreadRequest(BaseModel):
    """Request to create a new thread."""
    metadata: Optional[dict] = None


class SendMessageRequest(BaseModel):
    """Request to send a message."""
    thread_id: Optional[str] = None
    content: str = Field(..., min_length=1, max_length=4000)


class ListThreadsRequest(BaseModel):
    """Request to list threads."""
    limit: int = Field(default=20, ge=1, le=100)
    offset: int = Field(default=0, ge=0)


class DeleteThreadRequest(BaseModel):
    """Request to delete a thread."""
    thread_id: str


class ChatKitActionRequest(BaseModel):
    """Generic ChatKit action request."""
    action: str
    payload: dict = Field(default_factory=dict)


# Helper to build context from request
async def build_context(
    user: AuthenticatedUser,
    request: Request,
    db: AsyncSession,
    thread_id: Optional[str] = None,
) -> RequestContext:
    """
    Build RequestContext from request data.

    Args:
        user: Authenticated user
        request: FastAPI request
        db: Database session
        thread_id: Optional thread ID

    Returns:
        RequestContext instance
    """
    # Extract headers
    headers = {k.lower(): v for k, v in request.headers.items()}

    # Get user stage from header or fetch from database based on progress
    user_stage = 1
    if stage_header := headers.get("x-user-stage"):
        try:
            user_stage = int(stage_header)
        except ValueError:
            pass
    else:
        # If no stage header provided, try to fetch from user's actual progress
        # Wrap in try/except because Better-Auth user IDs may not be UUIDs
        try:
            from sqlalchemy import select
            from src.core.learning.models import Progress, Stage

            result = await db.execute(
                select(Progress).where(Progress.user_id == user.id)
            )
            progress = result.scalar_one_or_none()

            if progress and progress.current_stage_id:
                stage_result = await db.execute(
                    select(Stage.number).where(Stage.id == progress.current_stage_id)
                )
                stage_number = stage_result.scalar_one_or_none()
                if stage_number is not None:
                    user_stage = stage_number
            else:
                from src.core.auth.models import User
                user_result = await db.execute(
                    select(User.current_stage).where(User.id == user.id)
                )
                user_stage_db = user_result.scalar_one_or_none()
                if user_stage_db is not None:
                    user_stage = user_stage_db
        except Exception as e:
            logger.debug(f"Could not fetch user stage from DB: {e}")
            # Default to stage 1 — this happens when Better-Auth user IDs
            # don't match the backend UUID schema
            await db.rollback()
            user_stage = 1

    return RequestContext.from_request(
        user_id=user.id,
        user_email=user.email,
        headers=headers,
        user_name=user.name,
        user_role=user.role,
        user_stage=user_stage,
        email_verified=user.email_verified,
        thread_id=thread_id,
    )


@router.post("")
async def chatkit_handler(
    request: Request,
    action_request: ChatKitActionRequest,
    user: AuthenticatedUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Handle ChatKit protocol requests.

    Supports actions:
    - threads.create: Create new conversation
    - threads.list: List user's conversations
    - threads.get: Get thread with messages
    - threads.delete: Delete a conversation
    - messages.history: Get message history
    - usage.stats: Get rate limit stats

    For streaming messages, use POST /api/v1/chatkit/stream
    """
    context = await build_context(user, request, db)
    retriever = get_retriever()
    server = IntelliStackChatKitServer(db, retriever=retriever)

    result = await server.handle_request(
        action=action_request.action,
        context=context,
        payload=action_request.payload,
    )

    if "error" in result:
        error_code = result.get("code", "UNKNOWN_ERROR")
        if error_code == "NOT_FOUND":
            raise HTTPException(status_code=404, detail=result["error"])
        elif error_code == "UNAUTHORIZED":
            raise HTTPException(status_code=403, detail=result["error"])
        else:
            raise HTTPException(status_code=400, detail=result["error"])

    return result


@router.post("/stream")
async def stream_message(
    request: Request,
    message_request: SendMessageRequest,
    user: AuthenticatedUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Send a message and stream the AI response.

    Returns Server-Sent Events (SSE) stream with:
    - event: thread - Thread info
    - event: message_saved - User message saved
    - event: response_start - AI response starting
    - event: chunk - Response text chunk
    - event: response_end - Response complete with metadata
    - event: error - Error occurred

    Rate limit headers included:
    - X-RateLimit-Limit
    - X-RateLimit-Remaining
    - X-RateLimit-Reset
    """
    context = await build_context(user, request, db, message_request.thread_id)
    retriever = get_retriever()
    server = IntelliStackChatKitServer(db, retriever=retriever)

    async def event_generator():
        """Generate SSE events."""
        try:
            async for event in server.stream_message(
                context=context,
                message=message_request.content,
                thread_id=message_request.thread_id,
            ):
                yield event
        except Exception as e:
            logger.exception(f"Stream error: {e}")
            yield f"event: error\ndata: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.get("/threads")
async def list_threads(
    request: Request,
    limit: int = 20,
    offset: int = 0,
    user: AuthenticatedUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    List user's conversation threads.

    Returns list of threads ordered by last activity.
    """
    context = await build_context(user, request, db)
    retriever = get_retriever()
    server = IntelliStackChatKitServer(db, retriever=retriever)

    return await server.handle_request(
        action="threads.list",
        context=context,
        payload={"limit": limit, "offset": offset},
    )


@router.get("/threads/{thread_id}")
async def get_thread(
    thread_id: str,
    request: Request,
    user: AuthenticatedUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Get a specific thread with its messages.
    """
    context = await build_context(user, request, db)
    retriever = get_retriever()
    server = IntelliStackChatKitServer(db, retriever=retriever)

    result = await server.handle_request(
        action="threads.get",
        context=context,
        payload={"thread_id": thread_id},
    )

    if "error" in result:
        if result.get("code") == "NOT_FOUND":
            raise HTTPException(status_code=404, detail=result["error"])
        raise HTTPException(status_code=400, detail=result["error"])

    return result


@router.delete("/threads/{thread_id}")
async def delete_thread(
    thread_id: str,
    request: Request,
    user: AuthenticatedUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Delete a conversation thread.
    """
    context = await build_context(user, request, db)
    retriever = get_retriever()
    server = IntelliStackChatKitServer(db, retriever=retriever)

    result = await server.handle_request(
        action="threads.delete",
        context=context,
        payload={"thread_id": thread_id},
    )

    if "error" in result:
        if result.get("code") == "NOT_FOUND":
            raise HTTPException(status_code=404, detail=result["error"])
        raise HTTPException(status_code=400, detail=result["error"])

    return result


@router.get("/usage")
async def get_usage_stats(
    request: Request,
    user: AuthenticatedUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Get current rate limit usage statistics.

    Returns:
    - used: Messages used today
    - limit: Daily message limit
    - remaining: Messages remaining
    - reset_at: When limit resets (ISO timestamp)
    - is_limited: Whether currently rate limited
    """
    context = await build_context(user, request, db)
    retriever = get_retriever()
    server = IntelliStackChatKitServer(db, retriever=retriever)

    return await server.handle_request(
        action="usage.stats",
        context=context,
        payload={},
    )
