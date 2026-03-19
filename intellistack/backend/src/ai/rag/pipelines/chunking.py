"""Text chunking utilities for content ingestion (FR-130)."""

import logging
from typing import List
import tiktoken

from src.ai.rag.config import QdrantConfig
from src.ai.rag.schemas import ContentChunk

logger = logging.getLogger(__name__)


class TextChunker:
    """
    Chunk text into overlapping segments for embeddings.

    Based on latest tiktoken patterns from Context7.
    """

    def __init__(self, config: QdrantConfig):
        """
        Initialize text chunker.

        Args:
            config: Qdrant configuration with chunking parameters
        """
        self.config = config
        self.chunk_size = config.chunk_size  # tokens
        self.chunk_overlap = config.chunk_overlap  # tokens

        # Use tiktoken for accurate token counting (Context7 pattern)
        try:
            self.encoding = tiktoken.encoding_for_model("gpt-4o")
        except Exception:
            # Fallback to cl100k_base encoding
            self.encoding = tiktoken.get_encoding("cl100k_base")

        logger.info(
            f"Initialized TextChunker with chunk_size={self.chunk_size}, "
            f"overlap={self.chunk_overlap}, encoding={self.encoding.name}"
        )

    def count_tokens(self, text: str) -> int:
        """
        Count tokens in text using tiktoken.

        Args:
            text: Text to count tokens

        Returns:
            Token count
        """
        return len(self.encoding.encode(text))

    def chunk_text(
        self,
        text: str,
        content_id: str,
        stage_id: str,
        stage_name: str,
        content_title: str,
        metadata: dict = None,
    ) -> List[ContentChunk]:
        """
        Chunk text with overlap (FR-130).

        Args:
            text: Text to chunk
            content_id: Content item ID
            stage_id: Stage ID
            stage_name: Stage name
            content_title: Content title
            metadata: Additional metadata

        Returns:
            List of content chunks
        """
        if not text or not text.strip():
            return []

        # Encode text to tokens
        tokens = self.encoding.encode(text)
        total_tokens = len(tokens)

        if total_tokens <= self.chunk_size:
            # Text fits in single chunk
            chunk_id = f"{content_id}_chunk_0"
            return [
                ContentChunk(
                    chunk_id=chunk_id,
                    content_id=content_id,
                    stage_id=stage_id,
                    stage_name=stage_name,
                    content_title=content_title,
                    chunk_index=0,
                    text=text,
                    tokens=total_tokens,
                    metadata=metadata or {},
                )
            ]

        # Split into overlapping chunks
        chunks = []
        chunk_index = 0
        start = 0

        while start < total_tokens:
            # Get chunk tokens
            end = min(start + self.chunk_size, total_tokens)
            chunk_tokens = tokens[start:end]

            # Decode to text
            chunk_text = self.encoding.decode(chunk_tokens)

            # Create chunk
            chunk_id = f"{content_id}_chunk_{chunk_index}"
            chunks.append(
                ContentChunk(
                    chunk_id=chunk_id,
                    content_id=content_id,
                    stage_id=stage_id,
                    stage_name=stage_name,
                    content_title=content_title,
                    chunk_index=chunk_index,
                    text=chunk_text,
                    tokens=len(chunk_tokens),
                    metadata=metadata or {},
                )
            )

            # Move to next chunk with overlap
            start += self.chunk_size - self.chunk_overlap
            chunk_index += 1

        logger.info(
            f"Chunked content {content_id}: {total_tokens} tokens → {len(chunks)} chunks"
        )
        return chunks
