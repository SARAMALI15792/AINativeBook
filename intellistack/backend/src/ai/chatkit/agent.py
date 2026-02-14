"""
ChatKit Socratic Tutor Agent

AI tutor using OpenAI Agents SDK with Socratic teaching methodology.
Integrates RAG for context-aware responses and stage-based access control.
"""

import logging
from typing import List, Optional, AsyncGenerator, Dict, Any

from agents import Agent, Runner, function_tool
from pydantic import BaseModel, Field

from src.ai.rag.retrieval import HybridRetriever
from src.ai.rag.schemas import RetrievalResult
from src.ai.tutor.guardrails import SocraticGuardrails
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


class RAGSearchResult(BaseModel):
    """Result from RAG search."""
    text: str
    source: str
    stage: int
    relevance: float


@function_tool
async def search_course_content(
    query: str,
    stage_limit: int = 5,
) -> List[RAGSearchResult]:
    """
    Search course content for relevant information.

    Only returns results from stages the student has unlocked.

    Args:
        query: Search query
        stage_limit: Maximum stage to search (based on user access)

    Returns:
        List of relevant content chunks with sources
    """
    # This is a placeholder - actual implementation uses HybridRetriever
    # The function is defined for the agent to use
    return []


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
        model: str = "gpt-4o",
    ):
        """
        Initialize tutor agent.

        Args:
            retriever: Hybrid retriever for RAG
            model: OpenAI model to use
        """
        self.retriever = retriever
        self.model = model

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
        # Build system prompt with context
        system_prompt = SOCRATIC_SYSTEM_PROMPT.format(
            accessible_stages=", ".join(f"Stage {s}" for s in context.accessible_stages),
            page_context=context.to_system_context(),
        )

        # Perform RAG retrieval if retriever available
        rag_context = ""
        citations = []

        if self.retriever:
            try:
                results = await self.retriever.retrieve(
                    query=user_message,
                    accessible_stage_ids=context.accessible_stage_ids,
                    top_k=5,
                )

                if results:
                    rag_context = self._format_rag_results(results)
                    citations = [
                        {"text": r.text[:100], "source": r.metadata.get("source", "Unknown")}
                        for r in results
                    ]
                    logger.info(f"RAG retrieved {len(results)} relevant chunks")
            except Exception as e:
                logger.error(f"RAG retrieval failed: {e}")

        # Build messages
        messages = []

        # Add system message
        if rag_context:
            system_prompt += f"\n\n## Relevant Course Content\n{rag_context}"

        messages.append({"role": "system", "content": system_prompt})

        # Add conversation history
        if conversation_history:
            for msg in conversation_history[-10:]:  # Last 10 messages
                messages.append({
                    "role": msg.get("role", "user"),
                    "content": msg.get("content", ""),
                })

        # Add current user message
        messages.append({"role": "user", "content": user_message})

        # Check for direct answer requests and add guardrail
        if self._is_direct_answer_request(user_message):
            messages.append({
                "role": "system",
                "content": SocraticGuardrails.get_redirect_response(),
            })

        # Create and run agent
        try:
            agent = Agent(
                name="SocraticTutor",
                model=self.model,
                instructions=system_prompt,
            )

            # Use Runner for streaming
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
        Stream response from OpenAI.

        Args:
            messages: Conversation messages

        Yields:
            Response text chunks
        """
        import openai

        client = openai.AsyncOpenAI()

        try:
            stream = await client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=True,
                temperature=0.7,
                max_tokens=1024,
            )

            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

        except Exception as e:
            logger.error(f"OpenAI streaming failed: {e}")
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
            source = result.metadata.get("source", "Unknown")
            stage = result.metadata.get("stage", "?")
            formatted.append(
                f"[{i}] Source: Stage {stage} - {source}\n{result.text}\n"
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
        self.tutor = SocraticTutorAgent(retriever=retriever)

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
