"""RAG API routes with streaming support (FR-066 to FR-080)."""

import json
import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.ai.rag.schemas import (
    ConversationCreate,
    MessageCreate,
    RAGQueryRequest,
    RAGQueryResponse,
    SourcePassage,
)
from src.ai.rag.service import RAGService
from src.core.auth.models import User
from src.core.auth.routes import get_current_active_user
from src.shared.database import get_session

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ai/rag", tags=["RAG Chatbot"])


def get_rag_service() -> RAGService:
    """Dependency to get RAG service instance."""
    return RAGService()


@router.post("/conversations", status_code=status.HTTP_201_CREATED)
async def create_conversation(
    conversation_data: ConversationCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
    rag_service: Annotated[RAGService, Depends(get_rag_service)],
):
    """
    Create new RAG conversation (FR-070).

    Args:
        conversation_data: Conversation creation data
        current_user: Current authenticated user
        db: Database session
        rag_service: RAG service instance

    Returns:
        Created conversation
    """
    conversation = await rag_service.create_conversation(
        db=db,
        user_id=str(current_user.id),
        title=conversation_data.title,
    )
    return {
        "id": conversation.id,
        "title": conversation.title,
        "created_at": conversation.created_at.isoformat(),
    }


@router.post("/query", response_model=RAGQueryResponse)
async def query_rag(
    query_request: RAGQueryRequest,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
    rag_service: Annotated[RAGService, Depends(get_rag_service)],
):
    """
    Query RAG chatbot with non-streaming response (FR-066).

    Args:
        query_request: Query request with question and context
        current_user: Current authenticated user
        db: Database session
        rag_service: RAG service instance

    Returns:
        RAG query response with answer and sources
    """
    try:
        response = await rag_service.query(
            db=db,
            user_id=str(current_user.id),
            query=query_request.query,
            conversation_id=query_request.conversation_id,
            selected_text=query_request.selected_text,
        )
        return response
    except Exception as e:
        logger.error(f"Error processing RAG query: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process query",
        )


@router.post("/query/stream")
async def query_rag_stream(
    query_request: RAGQueryRequest,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
    rag_service: Annotated[RAGService, Depends(get_rag_service)],
):
    """
    Query RAG chatbot with Server-Sent Events streaming (FR-069, FR-135).

    Based on FastAPI SSE streaming patterns.

    Args:
        query_request: Query request
        current_user: Current authenticated user
        db: Database session
        rag_service: RAG service instance

    Returns:
        StreamingResponse with SSE format
    """

    async def event_generator():
        """Generate SSE events from stream chunks."""
        try:
            async for chunk in rag_service.query_stream(
                db=db,
                user_id=str(current_user.id),
                query=query_request.query,
                conversation_id=query_request.conversation_id,
                selected_text=query_request.selected_text,
            ):
                # Format as SSE (Server-Sent Events)
                data = {
                    "content": chunk.content,
                    "is_final": chunk.is_final,
                    "sources": chunk.sources,
                    "message_id": chunk.message_id,
                }
                yield f"data: {json.dumps(data)}\n\n"

        except Exception as e:
            logger.error(f"Error in stream: {e}", exc_info=True)
            error_data = {
                "error": "Stream processing failed",
                "content": "",
                "is_final": True,
            }
            yield f"data: {json.dumps(error_data)}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # Disable nginx buffering
        },
    )


@router.post("/highlight-query")
async def highlight_query(
    query_request: RAGQueryRequest,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
    rag_service: Annotated[RAGService, Depends(get_rag_service)],
):
    """
    Query based on highlighted/selected text (FR-068).

    Args:
        query_request: Query with selected_text field
        current_user: Current authenticated user
        db: Database session
        rag_service: RAG service instance

    Returns:
        Query response
    """
    if not query_request.selected_text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="selected_text is required for highlight queries",
        )

    response = await rag_service.query(
        db=db,
        user_id=str(current_user.id),
        query=query_request.query,
        conversation_id=query_request.conversation_id,
        selected_text=query_request.selected_text,
    )
    return response


@router.get("/sources/{message_id}")
async def get_message_sources(
    message_id: str,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
    rag_service: Annotated[RAGService, Depends(get_rag_service)],
):
    """
    Get source passages used for a message (FR-075).

    Args:
        message_id: Message ID
        current_user: Current authenticated user
        db: Database session
        rag_service: RAG service instance

    Returns:
        List of source passages with citations
    """
    try:
        passages = await rag_service.get_source_passages(
            db=db,
            message_id=message_id,
        )
        return {"sources": passages}
    except Exception as e:
        logger.error(f"Error fetching sources: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sources not found for message",
        )


@router.get("/health")
async def rag_health_check(
    rag_service: Annotated[RAGService, Depends(get_rag_service)],
):
    """
    Check RAG system health (vector store, LLM client).

    Returns:
        Health status
    """
    try:
        # Check vector store
        collection_info = await rag_service.vector_store.get_collection_info()

        return {
            "status": "healthy",
            "vector_store": {
                "status": collection_info.get("status"),
                "points_count": collection_info.get("points_count", 0),
            },
            "llm_client": "configured",
        }
    except Exception as e:
        logger.error(f"RAG health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
        }
