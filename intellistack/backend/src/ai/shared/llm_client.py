"""LLM client abstraction for OpenAI with streaming support."""

import os
from typing import AsyncIterator, List, Optional
import logging

from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionChunk

logger = logging.getLogger(__name__)


class LLMClient:
    """
    OpenAI LLM client with streaming support (FR-069, FR-135).

    Based on latest OpenAI Python SDK patterns from Context7.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize LLM client.

        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required")

        self.client = AsyncOpenAI(api_key=self.api_key)
        self.embedding_model = "text-embedding-3-small"
        self.chat_model = "gpt-4o"
        self.embedding_dimensions = 1536

    async def create_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for text using text-embedding-3-small.

        Args:
            text: Text to embed

        Returns:
            List[float]: Embedding vector (1536 dimensions)
        """
        try:
            response = await self.client.embeddings.create(
                model=self.embedding_model,
                input=text,
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Error creating embedding: {e}")
            raise

    async def create_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts in batch.

        Args:
            texts: List of texts to embed

        Returns:
            List of embedding vectors
        """
        try:
            response = await self.client.embeddings.create(
                model=self.embedding_model,
                input=texts,
            )
            # Sort by index to maintain order
            sorted_data = sorted(response.data, key=lambda x: x.index)
            return [item.embedding for item in sorted_data]
        except Exception as e:
            logger.error(f"Error creating batch embeddings: {e}")
            raise

    async def chat_completion_stream(
        self,
        messages: List[dict],
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> AsyncIterator[str]:
        """
        Stream chat completion responses (FR-069).

        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate

        Yields:
            Content delta strings as they arrive
        """
        try:
            async with self.client.chat.completions.stream(
                model=self.chat_model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True,
            ) as stream:
                async for event in stream:
                    if event.type == "content.delta" and event.content:
                        yield event.content
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
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate

        Returns:
            Complete response text
        """
        try:
            response = await self.client.chat.completions.create(
                model=self.chat_model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content or ""
        except Exception as e:
            logger.error(f"Error in chat completion: {e}")
            raise
