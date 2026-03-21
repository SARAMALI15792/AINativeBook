"""
ChatKit Socratic Tutor Agent

AI tutor using Socratic teaching methodology.
Integrates RAG for context-aware responses and stage-based access control.
Uses Google Gemini via LLMClient for streaming generation.
"""

import logging
from typing import List, Optional, AsyncGenerator, Dict, Any

from src.ai.rag.retrieval import HybridRetriever
from src.ai.rag.schemas import RetrievalResult
from src.ai.tutor.guardrails import SocraticGuardrails
from src.ai.shared.llm_client import LLMClient
from .context import RequestContext

logger = logging.getLogger(__name__)


# System prompt for Socratic teaching
SOCRATIC_SYSTEM_PROMPT = """You are an AI tutor for IntelliStack, an educational platform for Physical AI & Humanoid Robotics.

## Teaching Philosophy
You follow the Socratic method: guide students to discover answers themselves through thoughtful questions.
- Never give direct answers to coding problems
- Ask guiding questions that lead to understanding
- Provide hints, not solutions
- Reference concepts the student should review
- Celebrate when students make progress

## Content Access Control
You can only reference content from stages the student has unlocked.
Student's accessible stages: {accessible_stages}
Only search and cite content from these stages.

## Current Context
{page_context}

## Response Guidelines
1. For conceptual questions: Ask clarifying questions, then guide to the answer
2. For debugging help: Help identify the problem through questions, suggest investigation steps
3. For code help: Explain concepts, suggest approaches, but don't write the solution
4. For direct answer requests: Redirect to learning by asking what they've tried

## Citation Format
When referencing course content, use: [Source: Stage X - Lesson Title]

Be encouraging, patient, and supportive. Learning takes time."""


class SocraticTutorAgent:
    """
    Socratic AI Tutor using OpenAI Agents SDK.

    Features:
    - Socratic teaching methodology
    - RAG-augmented responses
    - Stage-based access control
    - Streaming responses
    """

    def __init__(
        self,
        retriever: Optional[HybridRetriever] = None,
        llm_client: Optional[LLMClient] = None,
    ):
        """
        Initialize tutor agent.

        Args:
            retriever: Hybrid retriever for RAG
            llm_client: Google Gemini LLM client for streaming generation
        """
        self.retriever = retriever
        self.llm_client = llm_client
        self._last_citations: List[Dict[str, Any]] = []

    async def generate_response(
        self,
        user_message: str,
        context: RequestContext,
        conversation_history: Optional[List[Dict[str, str]]] = None,
    ) -> AsyncGenerator[str, None]:
        """
        Generate a streaming Socratic response.

        Args:
            user_message: User's message
            context: Request context with user info and page context
            conversation_history: Previous messages in the thread

        Yields:
            Response text chunks
        """
        # Reset citations for this request
        self._last_citations = []

        # Build system prompt with context
        system_prompt = SOCRATIC_SYSTEM_PROMPT.format(
            accessible_stages=", ".join(f"Stage {s}" for s in context.accessible_stages),
            page_context=context.to_system_context(),
        )

        # Perform RAG retrieval if retriever available
        rag_context = ""

        if self.retriever:
            try:
                results = await self.retriever.retrieve(
                    query=user_message,
                    accessible_stage_ids=context.accessible_stage_ids,
                    top_k=5,
                )

                if results:
                    rag_context = self._format_rag_results(results)
                    self._last_citations = [
                        {
                            "stage_name": r.stage_name,
                            "content_title": r.content_title,
                            "text": r.text[:200],
                            "score": r.score,
                        }
                        for r in results
                    ]
                    logger.info(f"RAG retrieved {len(results)} relevant chunks")
            except Exception as e:
                logger.error(f"RAG retrieval failed: {e}")

        # Build messages
        messages = []

        # Merge RAG context and guardrail into the single system prompt
        # (Gemini only accepts one system instruction; mid-conversation system
        #  messages are not valid and overwrite the main prompt in _convert_messages)
        if rag_context:
            system_prompt += f"\n\n## Relevant Course Content\n{rag_context}"

        if self._is_direct_answer_request(user_message):
            from src.ai.tutor.models import IntentType
            guardrail = SocraticGuardrails.generate_redirect_response(
                intent=IntentType.CONCEPT,
                original_request=user_message,
            )
            system_prompt += f"\n\n## Guardrail\n{guardrail}"

        messages.append({"role": "system", "content": system_prompt})

        # Add conversation history (Gemini requires alternating user/model turns)
        if conversation_history:
            last_role = None
            for msg in conversation_history[-10:]:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                # Skip empty messages or consecutive same-role turns
                if not content or role == last_role:
                    continue
                messages.append({"role": role, "content": content})
                last_role = role

        # Add current user message
        messages.append({"role": "user", "content": user_message})

        # Stream response via Gemini
        try:
            async for chunk in self._stream_response(messages):
                yield chunk

        except Exception as e:
            logger.error(f"Agent execution failed: {e}")
            yield f"I apologize, but I encountered an error. Please try again. Error: {str(e)}"

    async def _stream_response(
        self,
        messages: List[Dict[str, str]],
    ) -> AsyncGenerator[str, None]:
        """
        Stream response from Google Gemini via LLMClient.

        Args:
            messages: OpenAI-style conversation messages

        Yields:
            Response text chunks
        """
        if self.llm_client is None:
            raise ValueError("LLMClient required. Pass llm_client to SocraticTutorAgent.__init__.")
        try:
            async for chunk in self.llm_client.chat_completion_stream(
                messages=messages,
                temperature=0.7,
                max_tokens=1024,
            ):
                yield chunk
        except Exception as e:
            logger.error(f"Gemini streaming failed: {e}")
            raise

    def _format_rag_results(self, results: List[RetrievalResult]) -> str:
        """
        Format RAG results for system prompt.

        Args:
            results: Retrieved content chunks

        Returns:
            Formatted context string
        """
        formatted = []
        for i, result in enumerate(results, 1):
            formatted.append(
                f"[{i}] Source: {result.stage_name} - {result.content_title}\n{result.text}\n"
            )
        return "\n".join(formatted)

    def _is_direct_answer_request(self, message: str) -> bool:
        """
        Check if message is requesting a direct answer.

        Args:
            message: User message

        Returns:
            True if requesting direct answer
        """
        direct_indicators = [
            "give me the answer",
            "tell me the solution",
            "write the code for me",
            "just solve it",
            "do it for me",
            "show me the answer",
        ]
        message_lower = message.lower()
        return any(indicator in message_lower for indicator in direct_indicators)


class ChatKitTutorAgent:
    """
    Wrapper for ChatKit integration with Socratic Tutor.

    Provides the interface expected by ChatKit server.
    """

    def __init__(self, retriever: Optional[HybridRetriever] = None):
        """
        Initialize ChatKit-compatible agent.

        Args:
            retriever: Hybrid retriever for RAG
        """
        llm_client = LLMClient()
        self.tutor = SocraticTutorAgent(
            retriever=retriever,
            llm_client=llm_client,
        )

    async def respond(
        self,
        user_message: str,
        context: RequestContext,
        history: List[Dict[str, str]] = None,
    ) -> AsyncGenerator[str, None]:
        """
        Generate streaming response for ChatKit.

        Args:
            user_message: User's message
            context: Request context
            history: Conversation history

        Yields:
            Response chunks
        """
        async for chunk in self.tutor.generate_response(
            user_message=user_message,
            context=context,
            conversation_history=history,
        ):
            yield chunk
