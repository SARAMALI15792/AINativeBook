"""RAG service layer for conversation management and query processing."""

import logging
from datetime import datetime, timezone
from typing import AsyncIterator, List, Optional
from uuid import uuid4

from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.ai.rag.config import get_qdrant_config
from src.ai.rag.models import RAGConversation, RAGMessage, RAGRetrieval
from src.ai.rag.retrieval import HybridRetriever
from src.ai.rag.schemas import (
    ConversationCreate,
    MessageCreate,
    RAGQueryResponse,
    SourcePassage,
    StreamChunk,
)
from src.ai.rag.vector_store import VectorStore
from src.ai.shared.llm_client import LLMClient
from src.ai.shared.prompts import RAG_SYSTEM_PROMPT, LOW_CONFIDENCE_MESSAGE
from src.core.learning.models import Progress

logger = logging.getLogger(__name__)


class RAGService:
    """
    RAG service for conversation management and query processing (FR-066 to FR-080).
    """

    def __init__(self):
        """Initialize RAG service."""
        self.config = get_qdrant_config()
        self.llm_client = LLMClient()
        self.vector_store = VectorStore(self.config)
        self.retriever = HybridRetriever(
            vector_store=self.vector_store,
            llm_client=self.llm_client,
            config=self.config,
        )

    async def create_conversation(
        self,
        db: AsyncSession,
        user_id: str,
        title: Optional[str] = None,
    ) -> RAGConversation:
        """
        Create new RAG conversation (FR-070).

        Args:
            db: Database session
            user_id: User ID
            title: Optional conversation title

        Returns:
            Created conversation
        """
        conversation = RAGConversation(
            user_id=user_id,
            title=title or "New Conversation",
        )
        db.add(conversation)
        await db.commit()
        await db.refresh(conversation)

        logger.info(f"Created RAG conversation {conversation.id} for user {user_id}")
        return conversation

    async def get_accessible_stage_ids(
        self,
        db: AsyncSession,
        user_id: str,
    ) -> List[str]:
        """
        Get stage IDs accessible to user (FR-078).

        Args:
            db: Database session
            user_id: User ID

        Returns:
            List of accessible stage IDs
        """
        # Get user's progress to determine unlocked stages
        result = await db.execute(
            select(Progress).where(Progress.user_id == user_id)
        )
        progress = result.scalar_one_or_none()

        if not progress:
            # New user - only access to Stage 1
            from src.core.learning.models import Stage
            result = await db.execute(
                select(Stage.id).where(Stage.number == 1)
            )
            stage_1_id = result.scalar_one_or_none()
            return [stage_1_id] if stage_1_id else []

        # TODO: Implement proper stage unlocking logic based on completion
        # For now, return all stages up to current stage
        from src.core.learning.models import Stage
        result = await db.execute(
            select(Stage.id).where(Stage.number <= (progress.current_stage_number or 1))
        )
        accessible_ids = [row[0] for row in result.all()]

        return accessible_ids

    async def query_stream(
        self,
        db: AsyncSession,
        user_id: str,
        query: str,
        conversation_id: Optional[str] = None,
        selected_text: Optional[str] = None,
    ) -> AsyncIterator[StreamChunk]:
        """
        Process query with streaming response (FR-069, FR-135).

        Args:
            db: Database session
            user_id: User ID
            query: User query
            conversation_id: Existing conversation ID or None for new
            selected_text: Selected text for context (FR-068)

        Yields:
            Stream chunks with content and metadata
        """
        # Create or get conversation
        if conversation_id:
            result = await db.execute(
                select(RAGConversation).where(RAGConversation.id == conversation_id)
            )
            conversation = result.scalar_one_or_none()
            if not conversation:
                raise ValueError(f"Conversation {conversation_id} not found")
        else:
            conversation = await self.create_conversation(
                db=db,
                user_id=user_id,
                title=query[:50],
            )

        # Get accessible stages (FR-078)
        accessible_stage_ids = await self.get_accessible_stage_ids(db, user_id)

        # Step 1: Retrieve relevant content
        logger.info(f"Retrieving content for query: {query[:50]}...")
        results, formatted_context = await self.retriever.retrieve_with_context(
            query=query,
            accessible_stage_ids=accessible_stage_ids,
            selected_text=selected_text,
        )

        if not results:
            # No relevant content found (FR-073)
            yield StreamChunk(
                content="I couldn't find relevant information in the available course content to answer your question. ",
                is_final=False,
            )
            yield StreamChunk(
                content="Please try rephrasing your question or ask your instructor for help.",
                is_final=True,
                sources=[],
            )
            return

        # Calculate confidence based on retrieval scores (FR-072)
        avg_score = sum(r.score for r in results) / len(results)
        confidence = min(avg_score, 1.0)

        # Step 2: Build conversation history (FR-070, FR-074)
        conversation_history = await self._get_conversation_history(db, conversation.id)

        # Build messages for LLM
        messages = [
            {"role": "system", "content": RAG_SYSTEM_PROMPT},
        ]

        # Add conversation history
        for msg in conversation_history[-5:]:  # Last 5 messages for context
            messages.append({
                "role": msg.role,
                "content": msg.content,
            })

        # Add current query with context
        user_message = f"Context from course materials:\n\n{formatted_context}\n\nStudent question: {query}"
        if selected_text:
            user_message = f"Selected text: {selected_text}\n\n{user_message}"

        messages.append({"role": "user", "content": user_message})

        # Step 3: Stream LLM response
        message_id = str(uuid4())
        full_response = []

        async for content_delta in self.llm_client.chat_completion_stream(
            messages=messages,
            temperature=0.7,
            max_tokens=1000,
        ):
            full_response.append(content_delta)
            yield StreamChunk(content=content_delta, is_final=False)

        # Prepare sources for citation (FR-067, FR-132)
        sources = [
            {
                "stage_name": r.stage_name,
                "content_title": r.content_title,
                "text_snippet": r.text[:200] + "..." if len(r.text) > 200 else r.text,
                "relevance_score": r.score,
            }
            for r in results
        ]

        # Add low confidence warning if needed (FR-072)
        if confidence < 0.7:
            full_response.append(f"\n\n{LOW_CONFIDENCE_MESSAGE}")

        # Final chunk with sources
        yield StreamChunk(
            content="",
            is_final=True,
            sources=sources,
            message_id=message_id,
        )

        # Step 4: Save conversation (FR-070, FR-079)
        await self._save_message(
            db=db,
            conversation_id=conversation.id,
            user_id=user_id,
            query=query,
            response="".join(full_response),
            confidence=confidence,
            sources=sources,
            results=results,
            selected_text=selected_text,
        )

    async def query(
        self,
        db: AsyncSession,
        user_id: str,
        query: str,
        conversation_id: Optional[str] = None,
        selected_text: Optional[str] = None,
    ) -> RAGQueryResponse:
        """
        Process query with non-streaming response.

        Args:
            db: Database session
            user_id: User ID
            query: User query
            conversation_id: Existing conversation ID
            selected_text: Selected text for context

        Returns:
            Query response with answer and sources
        """
        # Collect all stream chunks
        chunks = []
        sources = []
        message_id = None

        async for chunk in self.query_stream(
            db=db,
            user_id=user_id,
            query=query,
            conversation_id=conversation_id,
            selected_text=selected_text,
        ):
            chunks.append(chunk.content)
            if chunk.is_final:
                sources = chunk.sources
                message_id = chunk.message_id

        answer = "".join(chunks)

        # Get conversation ID
        result = await db.execute(
            select(RAGConversation)
            .where(RAGConversation.user_id == user_id)
            .order_by(desc(RAGConversation.created_at))
            .limit(1)
        )
        conversation = result.scalar_one()

        return RAGQueryResponse(
            answer=answer,
            sources=sources,
            confidence=0.8,  # TODO: Calculate properly
            conversation_id=conversation.id,
            message_id=message_id or str(uuid4()),
            retrieved_chunks=len(sources),
        )

    async def _get_conversation_history(
        self,
        db: AsyncSession,
        conversation_id: str,
    ) -> List[RAGMessage]:
        """Get conversation message history."""
        result = await db.execute(
            select(RAGMessage)
            .where(RAGMessage.conversation_id == conversation_id)
            .order_by(RAGMessage.created_at)
        )
        return result.scalars().all()

    async def _save_message(
        self,
        db: AsyncSession,
        conversation_id: str,
        user_id: str,
        query: str,
        response: str,
        confidence: float,
        sources: List[dict],
        results: List,
        selected_text: Optional[str],
    ):
        """Save user query and assistant response to database."""
        # Save user message
        user_msg = RAGMessage(
            conversation_id=conversation_id,
            user_id=user_id,
            role="user",
            content=query,
            query=query,
            selected_text=selected_text,
        )
        db.add(user_msg)

        # Save assistant message
        assistant_msg = RAGMessage(
            conversation_id=conversation_id,
            user_id=user_id,
            role="assistant",
            content=response,
            confidence=confidence,
            sources={"sources": sources},
            retrieved_count=len(results),
        )
        db.add(assistant_msg)
        await db.flush()

        # Save retrievals for analytics (FR-079)
        for result in results:
            retrieval = RAGRetrieval(
                message_id=assistant_msg.id,
                chunk_id=result.chunk_id,
                content_id=result.content_id,
                stage_id=result.stage_id,
                relevance_score=result.score,
                rerank_score=result.metadata.get("rerank_score"),
            )
            db.add(retrieval)

        await db.commit()
        logger.info(f"Saved conversation messages for conversation {conversation_id}")

    async def get_source_passages(
        self,
        db: AsyncSession,
        message_id: str,
    ) -> List[SourcePassage]:
        """
        Get source passages used for a message (FR-075).

        Args:
            db: Database session
            message_id: Message ID

        Returns:
            List of source passages
        """
        result = await db.execute(
            select(RAGRetrieval)
            .where(RAGRetrieval.message_id == message_id)
            .order_by(desc(RAGRetrieval.relevance_score))
        )
        retrievals = result.scalars().all()

        # Fetch full content for each retrieval
        passages = []
        for retrieval in retrievals:
            # TODO: Fetch actual content from vector store or database
            passages.append(
                SourcePassage(
                    stage_name="Stage Name",  # Placeholder
                    content_title="Content Title",  # Placeholder
                    text="Source passage text...",  # Placeholder
                    relevance_score=retrieval.relevance_score,
                    url=None,
                )
            )

        return passages

    async def close(self):
        """Clean up resources."""
        await self.vector_store.close()
