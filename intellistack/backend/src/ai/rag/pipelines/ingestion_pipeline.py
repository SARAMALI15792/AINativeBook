"""Content ingestion pipeline for RAG system."""

import logging
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.ai.rag.config import get_qdrant_config
from src.ai.rag.pipelines.chunking import TextChunker
from src.ai.rag.schemas import ContentChunk
from src.ai.rag.vector_store import VectorStore
from src.ai.shared.llm_client import LLMClient
from src.core.learning.models import ContentItem, Stage

logger = logging.getLogger(__name__)


class IngestionPipeline:
    """
    Content ingestion pipeline for indexing to vector store (FR-130).

    Processes content items into chunks, generates embeddings, and stores in Qdrant.
    """

    def __init__(self):
        """Initialize ingestion pipeline."""
        self.config = get_qdrant_config()
        self.chunker = TextChunker(self.config)
        self.vector_store = VectorStore(self.config)
        self.llm_client = LLMClient()

    async def initialize(self):
        """Ensure vector store collection exists."""
        await self.vector_store.ensure_collection_exists()

    async def ingest_content_item(
        self,
        db: AsyncSession,
        content_id: str,
        force_reindex: bool = False,
    ) -> int:
        """
        Ingest single content item (FR-130).

        Args:
            db: Database session
            content_id: Content item ID
            force_reindex: Force re-indexing if already indexed

        Returns:
            Number of chunks created
        """
        # Fetch content item with stage info
        result = await db.execute(
            select(ContentItem, Stage)
            .join(Stage, ContentItem.stage_id == Stage.id)
            .where(ContentItem.id == content_id)
        )
        row = result.first()

        if not row:
            logger.warning(f"Content item not found: {content_id}")
            return 0

        content_item, stage = row

        # Check if content has text to index
        # TODO: Load actual content from content_path or database
        # For now, using title and type as placeholder
        text_to_index = f"{content_item.title}\n\nType: {content_item.content_type}"

        if not text_to_index or not text_to_index.strip():
            logger.warning(f"No text to index for content {content_id}")
            return 0

        # Delete existing chunks if force reindex
        if force_reindex:
            await self.vector_store.delete_by_content_id(content_id)
            logger.info(f"Deleted existing chunks for content {content_id}")

        # Chunk text
        chunks = self.chunker.chunk_text(
            text=text_to_index,
            content_id=content_id,
            stage_id=stage.id,
            stage_name=stage.name,
            content_title=content_item.title,
            metadata={
                "content_type": content_item.content_type,
                "order": content_item.order,
                "estimated_minutes": content_item.estimated_minutes,
            },
        )

        if not chunks:
            logger.warning(f"No chunks created for content {content_id}")
            return 0

        # Generate embeddings in batch
        logger.info(f"Generating embeddings for {len(chunks)} chunks...")
        chunk_texts = [chunk.text for chunk in chunks]
        embeddings = await self.llm_client.create_embeddings_batch(chunk_texts)

        # Upsert to vector store
        await self.vector_store.upsert_chunks(chunks, embeddings)

        logger.info(f"Indexed content {content_id}: {len(chunks)} chunks")
        return len(chunks)

    async def ingest_stage(
        self,
        db: AsyncSession,
        stage_id: str,
        force_reindex: bool = False,
    ) -> tuple[int, int]:
        """
        Ingest all content items in a stage.

        Args:
            db: Database session
            stage_id: Stage ID
            force_reindex: Force re-indexing

        Returns:
            Tuple of (items_indexed, total_chunks)
        """
        # Fetch all content items in stage
        result = await db.execute(
            select(ContentItem)
            .where(ContentItem.stage_id == stage_id)
            .where(ContentItem.is_active == True)
            .order_by(ContentItem.order)
        )
        content_items = result.scalars().all()

        items_indexed = 0
        total_chunks = 0

        for content_item in content_items:
            try:
                chunks = await self.ingest_content_item(
                    db=db,
                    content_id=content_item.id,
                    force_reindex=force_reindex,
                )
                items_indexed += 1
                total_chunks += chunks
            except Exception as e:
                logger.error(f"Failed to index content {content_item.id}: {e}")

        logger.info(
            f"Indexed stage {stage_id}: {items_indexed} items, {total_chunks} chunks"
        )
        return items_indexed, total_chunks

    async def ingest_all_content(
        self,
        db: AsyncSession,
        force_reindex: bool = False,
    ) -> tuple[int, int]:
        """
        Ingest all active content items (FR-130).

        Args:
            db: Database session
            force_reindex: Force re-indexing

        Returns:
            Tuple of (items_indexed, total_chunks)
        """
        # Fetch all stages
        result = await db.execute(
            select(Stage)
            .where(Stage.is_active == True)
            .order_by(Stage.number)
        )
        stages = result.scalars().all()

        total_items = 0
        total_chunks = 0

        for stage in stages:
            try:
                items, chunks = await self.ingest_stage(
                    db=db,
                    stage_id=stage.id,
                    force_reindex=force_reindex,
                )
                total_items += items
                total_chunks += chunks
            except Exception as e:
                logger.error(f"Failed to index stage {stage.id}: {e}")

        logger.info(
            f"Completed full ingestion: {total_items} items, {total_chunks} chunks"
        )
        return total_items, total_chunks

    async def close(self):
        """Clean up resources."""
        await self.vector_store.close()
