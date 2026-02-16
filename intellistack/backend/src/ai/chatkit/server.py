"""
ChatKit Server Implementation

Main server that handles ChatKit protocol requests,
integrates with the Socratic tutor agent, and manages streaming responses.
"""

import json
import logging
import uuid
from datetime import datetime
from typing import Optional, Dict, Any, AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from .store import PostgresChatKitStore
from .context import RequestContext
from .rate_limiter import RateLimiter, RateLimitResult
from .agent import ChatKitTutorAgent
from .models import AiUsageMetric, AuthEventLog

logger = logging.getLogger(__name__)


class IntelliStackChatKitServer:
    """
    ChatKit server for IntelliStack platform.

    Handles:
    - Thread management (create, list, delete)
    - Message sending with streaming
    - Rate limiting
    - Usage metrics tracking
    """

    def __init__(
        self,
        db_session: AsyncSession,
        retriever=None,
    ):
        """
        Initialize ChatKit server.

        Args:
            db_session: SQLAlchemy async session
            retriever: Optional HybridRetriever for RAG
        """
        self.db = db_session
        self.store = PostgresChatKitStore(db_session)
        self.rate_limiter = RateLimiter(db_session)
        self.agent = ChatKitTutorAgent(retriever=retriever)

    async def handle_request(
        self,
        action: str,
        context: RequestContext,
        payload: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Handle a ChatKit protocol request.

        Args:
            action: Action to perform (threads.create, messages.send, etc.)
            context: Request context with user info
            payload: Request payload

        Returns:
            Response dict
        """
        # Route to appropriate handler
        handlers = {
            "threads.create": self._handle_create_thread,
            "threads.list": self._handle_list_threads,
            "threads.get": self._handle_get_thread,
            "threads.delete": self._handle_delete_thread,
            "messages.send": self._handle_send_message,
            "messages.history": self._handle_message_history,
            "usage.stats": self._handle_usage_stats,
        }

        handler = handlers.get(action)
        if not handler:
            return {"error": f"Unknown action: {action}", "code": "INVALID_ACTION"}

        try:
            return await handler(context, payload)
        except Exception as e:
            logger.exception(f"Handler error for {action}: {e}")
            return {"error": str(e), "code": "INTERNAL_ERROR"}

    async def _handle_create_thread(
        self,
        context: RequestContext,
        payload: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Create a new conversation thread."""
        thread = await self.store.create_thread(
            user_id=context.user_id,
            metadata={
                "page_url": context.page_context.url,
                "page_title": context.page_context.title,
                "created_at": datetime.utcnow().isoformat(),
            },
            course_id=context.page_context.course_id,
            lesson_stage=context.user_stage,
        )

        return {
            "thread": {
                "id": thread.id,
                "title": thread.title,
                "created_at": thread.created_at.isoformat(),
            }
        }

    async def _handle_list_threads(
        self,
        context: RequestContext,
        payload: Dict[str, Any],
    ) -> Dict[str, Any]:
        """List user's conversation threads."""
        limit = payload.get("limit", 20)
        offset = payload.get("offset", 0)

        threads = await self.store.list_threads(
            user_id=context.user_id,
            limit=limit,
            offset=offset,
        )

        return {
            "threads": [
                {
                    "id": t.id,
                    "title": t.title or "New conversation",
                    "updated_at": t.updated_at.isoformat(),
                    "message_count": 0,  # Avoid lazy-loading items in list view
                }
                for t in threads
            ]
        }

    async def _handle_get_thread(
        self,
        context: RequestContext,
        payload: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Get a specific thread with messages."""
        thread_id = payload.get("thread_id")
        if not thread_id:
            return {"error": "thread_id required", "code": "MISSING_PARAM"}

        thread = await self.store.load_thread(thread_id)
        if not thread:
            return {"error": "Thread not found", "code": "NOT_FOUND"}

        # Verify ownership
        if thread.user_id != context.user_id:
            return {"error": "Not authorized", "code": "UNAUTHORIZED"}

        return {
            "thread": {
                "id": thread.id,
                "title": thread.title,
                "created_at": thread.created_at.isoformat(),
                "updated_at": thread.updated_at.isoformat(),
            },
            "messages": [
                {
                    "id": item.id,
                    "role": item.role,
                    "content": item.content,
                    "created_at": item.created_at.isoformat(),
                }
                for item in (thread.items or [])
            ],
        }

    async def _handle_delete_thread(
        self,
        context: RequestContext,
        payload: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Delete a conversation thread."""
        thread_id = payload.get("thread_id")
        if not thread_id:
            return {"error": "thread_id required", "code": "MISSING_PARAM"}

        deleted = await self.store.delete_thread(thread_id, context.user_id)
        if not deleted:
            return {"error": "Thread not found or not authorized", "code": "NOT_FOUND"}

        return {"success": True}

    async def _handle_message_history(
        self,
        context: RequestContext,
        payload: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Get message history for a thread."""
        thread_id = payload.get("thread_id")
        limit = payload.get("limit", 50)
        before_id = payload.get("before_id")

        if not thread_id:
            return {"error": "thread_id required", "code": "MISSING_PARAM"}

        # Verify ownership
        thread = await self.store.load_thread(thread_id)
        if not thread or thread.user_id != context.user_id:
            return {"error": "Thread not found", "code": "NOT_FOUND"}

        items = await self.store.load_thread_items(
            thread_id=thread_id,
            limit=limit,
            before_id=before_id,
        )

        return {
            "messages": [
                {
                    "id": item.id,
                    "role": item.role,
                    "content": item.content,
                    "created_at": item.created_at.isoformat(),
                }
                for item in items
            ]
        }

    async def _handle_usage_stats(
        self,
        context: RequestContext,
        payload: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Get rate limit usage statistics."""
        usage = await self.rate_limiter.get_usage(context.user_id, context.user_role)
        return {"usage": usage}

    async def _handle_send_message(
        self,
        context: RequestContext,
        payload: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Handle message send - returns immediately, streaming handled separately.

        For actual streaming, use stream_message method.
        """
        return {
            "info": "Use stream_message for streaming responses",
            "rate_limit": await self.rate_limiter.get_usage(
                context.user_id, context.user_role
            ),
        }

    async def stream_message(
        self,
        context: RequestContext,
        message: str,
        thread_id: Optional[str] = None,
    ) -> AsyncGenerator[str, None]:
        """
        Stream a response to a user message.

        This is the main method for sending messages and getting AI responses.

        Args:
            context: Request context
            message: User's message
            thread_id: Optional thread ID (creates new if not provided)

        Yields:
            Server-Sent Events formatted response chunks
        """
        start_time = datetime.utcnow()

        # Check rate limit
        rate_result = await self.rate_limiter.check_limit(
            context.user_id, context.user_role
        )

        if not rate_result.allowed:
            yield self._format_sse_event("error", {
                "code": "RATE_LIMITED",
                "message": rate_result.message,
                "reset_at": rate_result.reset_timestamp,
            })
            return

        # Update context with rate limit info
        context.rate_limit_remaining = rate_result.remaining
        context.rate_limit_reset = rate_result.reset_timestamp

        try:
            # Create or get thread
            if thread_id:
                thread = await self.store.load_thread(thread_id)
                if not thread or thread.user_id != context.user_id:
                    yield self._format_sse_event("error", {
                        "code": "NOT_FOUND",
                        "message": "Thread not found",
                    })
                    return
            else:
                thread = await self.store.create_thread(
                    user_id=context.user_id,
                    metadata={
                        "page_url": context.page_context.url,
                        "page_title": context.page_context.title,
                    },
                    course_id=context.page_context.course_id,
                    lesson_stage=context.user_stage,
                )
                thread_id = thread.id

            # Send thread info
            yield self._format_sse_event("thread", {
                "id": thread_id,
                "title": thread.title,
            })

            # Save user message
            user_item = await self.store.save_thread_item(
                thread_id=thread_id,
                role="user",
                content=message,
                metadata={
                    "page_context": {
                        "url": context.page_context.url,
                        "title": context.page_context.title,
                        "selected_text": context.page_context.selected_text,
                    }
                },
            )

            yield self._format_sse_event("message_saved", {
                "id": user_item.id,
                "role": "user",
            })

            # Get conversation history
            history = await self.store.load_thread_items(thread_id, limit=20)
            history_dicts = [
                {"role": item.role, "content": item.content}
                for item in history[:-1]  # Exclude current message
            ]

            # Stream response
            response_chunks = []
            yield self._format_sse_event("response_start", {})

            async for chunk in self.agent.respond(
                user_message=message,
                context=context,
                history=history_dicts,
            ):
                response_chunks.append(chunk)
                yield self._format_sse_event("chunk", {"text": chunk})

            full_response = "".join(response_chunks)

            # Save assistant response
            assistant_item = await self.store.save_thread_item(
                thread_id=thread_id,
                role="assistant",
                content=full_response,
                metadata={
                    "model": "gpt-4o",
                    "generation_time_ms": int(
                        (datetime.utcnow() - start_time).total_seconds() * 1000
                    ),
                },
            )

            # Increment rate limit
            new_rate = await self.rate_limiter.increment(
                context.user_id, context.user_role
            )

            # Track usage metrics
            await self._track_usage(
                user_id=context.user_id,
                response_time_ms=int(
                    (datetime.utcnow() - start_time).total_seconds() * 1000
                ),
            )

            yield self._format_sse_event("response_end", {
                "message_id": assistant_item.id,
                "rate_limit": {
                    "remaining": new_rate.remaining,
                    "limit": new_rate.limit,
                    "reset_at": new_rate.reset_timestamp,
                },
            })

        except Exception as e:
            logger.exception(f"Stream error: {e}")
            yield self._format_sse_event("error", {
                "code": "STREAM_ERROR",
                "message": str(e),
            })

    def _format_sse_event(self, event_type: str, data: Dict[str, Any]) -> str:
        """
        Format data as Server-Sent Events.

        Args:
            event_type: Event type name
            data: Event data

        Returns:
            SSE formatted string
        """
        return f"event: {event_type}\ndata: {json.dumps(data)}\n\n"

    async def _track_usage(
        self,
        user_id: str,
        response_time_ms: int,
        error: bool = False,
    ):
        """
        Track AI usage metrics.

        Args:
            user_id: User ID
            response_time_ms: Response generation time in ms
            error: Whether this was an error
        """
        try:
            # Get or create today's metric
            today = datetime.utcnow().date()

            from sqlalchemy import select, and_

            stmt = select(AiUsageMetric).where(
                and_(
                    AiUsageMetric.user_id == user_id,
                    AiUsageMetric.date >= datetime.combine(today, datetime.min.time()),
                    AiUsageMetric.date < datetime.combine(today, datetime.max.time()),
                )
            )
            result = await self.db.execute(stmt)
            metric = result.scalar_one_or_none()

            if not metric:
                metric = AiUsageMetric(
                    id=str(uuid.uuid4()),
                    user_id=user_id,
                    message_count=0,
                    total_tokens=0,
                    input_tokens=0,
                    output_tokens=0,
                    average_response_time_ms=0,
                    error_count=0,
                    date=datetime.utcnow(),
                )
                self.db.add(metric)

            # Update metrics
            metric.message_count += 1
            if error:
                metric.error_count += 1

            # Update average response time
            total_time = metric.average_response_time_ms * (metric.message_count - 1)
            metric.average_response_time_ms = (total_time + response_time_ms) // metric.message_count

            await self.db.commit()

        except Exception as e:
            logger.error(f"Failed to track usage: {e}")
