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

from src.shared.database import get_db
from src.core.auth.dependencies import (
    get_current_user,
    require_verified_email,
    AuthenticatedUser,
)
from .server import IntelliStackChatKitServer
from .context import RequestContext, PageContext

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/chatkit", tags=["chatkit"])


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
def build_context(
    user: AuthenticatedUser,
    request: Request,
    thread_id: Optional[str] = None,
) -> RequestContext:
    """
    Build RequestContext from request data.

    Args:
        user: Authenticated user
        request: FastAPI request
        thread_id: Optional thread ID

    Returns:
        RequestContext instance
    """
    # Extract headers
    headers = {k.lower(): v for k, v in request.headers.items()}

    # Get user stage from header or default
    user_stage = 1
    if stage_header := headers.get("x-user-stage"):
        try:
            user_stage = int(stage_header)
        except ValueError:
            pass

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
    # Verify email for AI features
    if not user.email_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email verification required to use AI tutor",
        )

    context = build_context(user, request)
    server = IntelliStackChatKitServer(db)

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
    # Verify email for AI features
    if not user.email_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email verification required to use AI tutor",
        )

    context = build_context(user, request, message_request.thread_id)
    server = IntelliStackChatKitServer(db)

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
    limit: int = 20,
    offset: int = 0,
    user: AuthenticatedUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    List user's conversation threads.

    Returns list of threads ordered by last activity.
    """
    context = build_context(user, Request(scope={"type": "http", "headers": []}))
    server = IntelliStackChatKitServer(db)

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
    context = build_context(user, request)
    server = IntelliStackChatKitServer(db)

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
    context = build_context(user, request)
    server = IntelliStackChatKitServer(db)

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
    context = build_context(user, request)
    server = IntelliStackChatKitServer(db)

    return await server.handle_request(
        action="usage.stats",
        context=context,
        payload={},
    )
