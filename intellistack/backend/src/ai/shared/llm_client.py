"""LLM client using Google Gemini AI (google-genai SDK) with streaming support."""

import logging
import os
from typing import AsyncIterator, List, Optional

from google import genai
from google.genai import types as genai_types

logger = logging.getLogger(__name__)


class LLMClient:
    """
    Google Gemini LLM client (FR-069, FR-135).

    Embeddings : models/text-embedding-004  (768 dimensions)
    Chat       : gemini-2.0-flash           (streaming + non-streaming)
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY is not set. Add it to your .env file before starting the server."
            )

        self.client = genai.Client(api_key=self.api_key)
        self.embedding_model = "models/gemini-embedding-001"
        self.chat_model = "gemini-2.0-flash"
        self.embedding_dimensions = 3072

    def _ensure_client(self) -> None:
        if self.client is None:
            raise ValueError(
                "GEMINI_API_KEY is not set. Add it to your .env file before starting the server."
            )

    # ── Embeddings ───────────────────────────────────────────────────────────

    async def create_embedding(self, text: str) -> List[float]:
        """
        Generate a single 768-dim embedding using text-embedding-004.

        Args:
            text: Text to embed

        Returns:
            768-dimensional float vector
        """
        self._ensure_client()
        try:
            response = await self.client.aio.models.embed_content(
                model=self.embedding_model,
                contents=text,
                config=genai_types.EmbedContentConfig(
                    task_type="RETRIEVAL_DOCUMENT",
                ),
            )
            return response.embeddings[0].values
        except Exception as e:
            logger.error(f"Error creating embedding: {e}")
            raise

    async def create_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts in one API call (order preserved).

        Args:
            texts: List of texts to embed

        Returns:
            List of 768-dimensional float vectors
        """
        self._ensure_client()
        try:
            response = await self.client.aio.models.embed_content(
                model=self.embedding_model,
                contents=texts,
                config=genai_types.EmbedContentConfig(
                    task_type="RETRIEVAL_DOCUMENT",
                ),
            )
            return [e.values for e in response.embeddings]
        except Exception as e:
            logger.error(f"Error creating batch embeddings: {e}")
            raise

    # ── Chat completions ──────────────────────────────────────────────────────

    async def chat_completion_stream(
        self,
        messages: List[dict],
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> AsyncIterator[str]:
        """
        Stream chat completion responses (FR-069).

        Args:
            messages: OpenAI-style [{role, content}] list.
                      Roles: "system" | "user" | "assistant"
            temperature: Sampling temperature
            max_tokens: Maximum output tokens

        Yields:
            Text delta strings as they arrive
        """
        self._ensure_client()
        try:
            system_instruction, contents = self._convert_messages(messages)

            stream = await self.client.aio.models.generate_content_stream(
                model=self.chat_model,
                contents=contents,
                config=genai_types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=temperature,
                    max_output_tokens=max_tokens,
                ),
            )
            async for chunk in stream:
                # Use candidates/parts directly to skip thought-only chunks
                # (gemini-2.5-flash+ thinking models emit thought parts with no text)
                try:
                    candidates = chunk.candidates or []
                    for candidate in candidates:
                        parts = getattr(candidate.content, "parts", []) or []
                        for part in parts:
                            if getattr(part, "thought", False):
                                continue  # skip internal reasoning
                            text = getattr(part, "text", None)
                            if text:
                                yield text
                except Exception:
                    # Fallback: try chunk.text directly
                    try:
                        if chunk.text:
                            yield chunk.text
                    except Exception:
                        pass
        except Exception as e:
            logger.error(f"Error in streaming chat completion: {e}")
            raise

    async def chat_completion(
        self,
        messages: List[dict],
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> str:
        """
        Non-streaming chat completion.

        Args:
            messages: OpenAI-style [{role, content}] list
            temperature: Sampling temperature
            max_tokens: Maximum output tokens

        Returns:
            Complete response text
        """
        self._ensure_client()
        try:
            system_instruction, contents = self._convert_messages(messages)

            response = await self.client.aio.models.generate_content(
                model=self.chat_model,
                contents=contents,
                config=genai_types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=temperature,
                    max_output_tokens=max_tokens,
                ),
            )
            return response.text or ""
        except Exception as e:
            logger.error(f"Error in chat completion: {e}")
            raise

    async def generate(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> str:
        """Convenience wrapper — generate from a single prompt string."""
        return await self.chat_completion(
            [{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
        )

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _convert_messages(
        self, messages: List[dict]
    ) -> tuple[Optional[str], List[dict]]:
        """
        Convert OpenAI-style messages to Gemini's contents format.

        Gemini differences vs OpenAI:
        - System prompt → GenerateContentConfig.system_instruction (not a message)
        - "assistant" role → "model" role
        - Each turn is {"role": ..., "parts": [{"text": ...}]}

        Returns:
            (system_instruction_or_None, gemini_contents_list)
        """
        system_instruction: Optional[str] = None
        contents: List[dict] = []

        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")

            if role == "system":
                # Concatenate multiple system messages instead of last-one-wins
                system_instruction = f"{system_instruction}\n\n{content}" if system_instruction else content
            elif role == "assistant":
                contents.append({"role": "model", "parts": [{"text": content}]})
            else:
                contents.append({"role": "user", "parts": [{"text": content}]})

        return system_instruction, contents
