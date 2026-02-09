"""Qdrant vector store client for RAG system."""

import logging
from typing import List, Optional

from qdrant_client import AsyncQdrantClient, models

from src.ai.rag.config import QdrantConfig, get_qdrant_config
from src.ai.rag.schemas import ContentChunk, RetrievalResult

logger = logging.getLogger(__name__)


class VectorStore:
    """
    Async Qdrant vector store for content retrieval (FR-071, FR-130).

    Based on latest qdrant-client patterns from Context7.
    """

    def __init__(self, config: Optional[QdrantConfig] = None):
        """
        Initialize vector store.

        Args:
            config: Qdrant configuration
        """
        self.config = config or get_qdrant_config()
        self.client = AsyncQdrantClient(
            url=f"http://{self.config.host}:{self.config.port}",
            api_key=self.config.api_key,
        )
        self.collection_name = self.config.collection_name

    async def ensure_collection_exists(self) -> None:
        """Create collection if it doesn't exist (FR-066)."""
        try:
            if not await self.client.collection_exists(self.collection_name):
                await self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=self.config.vector_size,
                        distance=models.Distance.COSINE,
                    ),
                )
                logger.info(f"Created Qdrant collection: {self.collection_name}")
            else:
                logger.debug(f"Collection already exists: {self.collection_name}")
        except Exception as e:
            logger.error(f"Error ensuring collection exists: {e}")
            raise

    async def upsert_chunks(self, chunks: List[ContentChunk], embeddings: List[List[float]]) -> None:
        """
        Upsert content chunks with embeddings (FR-130).

        Args:
            chunks: List of content chunks
            embeddings: Corresponding embedding vectors
        """
        try:
            points = [
                models.PointStruct(
                    id=chunk.chunk_id,
                    vector=embedding,
                    payload={
                        "content_id": chunk.content_id,
                        "stage_id": chunk.stage_id,
                        "stage_name": chunk.stage_name,
                        "content_title": chunk.content_title,
                        "chunk_index": chunk.chunk_index,
                        "text": chunk.text,
                        "tokens": chunk.tokens,
                        "metadata": chunk.metadata,
                    },
                )
                for chunk, embedding in zip(chunks, embeddings)
            ]

            await self.client.upsert(
                collection_name=self.collection_name,
                points=points,
            )
            logger.info(f"Upserted {len(points)} chunks to Qdrant")
        except Exception as e:
            logger.error(f"Error upserting chunks: {e}")
            raise

    async def search(
        self,
        query_vector: List[float],
        limit: int = 10,
        stage_filter: Optional[List[str]] = None,
        min_score: Optional[float] = None,
    ) -> List[RetrievalResult]:
        """
        Semantic search using query vector (FR-071, FR-078).

        Args:
            query_vector: Query embedding vector
            limit: Maximum results to return
            stage_filter: Filter by accessible stage IDs (FR-078)
            min_score: Minimum relevance score threshold

        Returns:
            List of retrieval results with scores
        """
        try:
            # Build filter for stage-based access control (FR-078)
            query_filter = None
            if stage_filter:
                query_filter = models.Filter(
                    must=[
                        models.FieldCondition(
                            key="stage_id",
                            match=models.MatchAny(any=stage_filter),
                        )
                    ]
                )

            # Perform search
            search_result = await self.client.query_points(
                collection_name=self.collection_name,
                query=query_vector,
                limit=limit,
                query_filter=query_filter,
                score_threshold=min_score or self.config.min_score,
            )

            # Convert to RetrievalResult
            results = []
            for point in search_result.points:
                if point.payload:
                    results.append(
                        RetrievalResult(
                            chunk_id=str(point.id),
                            content_id=point.payload["content_id"],
                            stage_id=point.payload["stage_id"],
                            stage_name=point.payload["stage_name"],
                            content_title=point.payload["content_title"],
                            text=point.payload["text"],
                            score=point.score or 0.0,
                            metadata=point.payload.get("metadata", {}),
                        )
                    )

            logger.info(f"Retrieved {len(results)} chunks for query")
            return results

        except Exception as e:
            logger.error(f"Error searching vector store: {e}")
            raise

    async def delete_by_content_id(self, content_id: str) -> None:
        """
        Delete all chunks for a content item.

        Args:
            content_id: Content item ID
        """
        try:
            await self.client.delete(
                collection_name=self.collection_name,
                points_selector=models.FilterSelector(
                    filter=models.Filter(
                        must=[
                            models.FieldCondition(
                                key="content_id",
                                match=models.MatchValue(value=content_id),
                            )
                        ]
                    )
                ),
            )
            logger.info(f"Deleted chunks for content_id: {content_id}")
        except Exception as e:
            logger.error(f"Error deleting chunks: {e}")
            raise

    async def get_collection_info(self) -> dict:
        """Get collection statistics."""
        try:
            info = await self.client.get_collection(self.collection_name)
            return {
                "vectors_count": info.vectors_count,
                "points_count": info.points_count,
                "status": info.status,
            }
        except Exception as e:
            logger.error(f"Error getting collection info: {e}")
            raise

    async def close(self):
        """Close client connection."""
        await self.client.close()
