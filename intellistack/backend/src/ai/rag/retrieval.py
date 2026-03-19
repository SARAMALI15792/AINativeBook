"""Hybrid retrieval with semantic search and optional reranking (FR-130, FR-131)."""

import logging
import os
from typing import List, Optional

try:
    import cohere
    COHERE_AVAILABLE = True
except ImportError:
    COHERE_AVAILABLE = False
    logging.warning("Cohere not installed. Reranking will be disabled.")

from src.ai.rag.config import QdrantConfig
from src.ai.rag.schemas import RetrievalResult
from src.ai.rag.vector_store import VectorStore
from src.ai.shared.llm_client import LLMClient

logger = logging.getLogger(__name__)


class HybridRetriever:
    """
    Hybrid retrieval with semantic search and Cohere reranking.

    Based on latest Cohere Python SDK patterns from Context7.
    """

    def __init__(
        self,
        vector_store: VectorStore,
        llm_client: LLMClient,
        config: QdrantConfig,
    ):
        """
        Initialize hybrid retriever.

        Args:
            vector_store: Vector store client
            llm_client: LLM client for embeddings
            config: Qdrant configuration
        """
        self.vector_store = vector_store
        self.llm_client = llm_client
        self.config = config

        # Initialize Cohere for reranking (FR-131)
        self.cohere_client = None
        cohere_api_key = os.getenv("COHERE_API_KEY")
        if COHERE_AVAILABLE and cohere_api_key:
            self.cohere_client = cohere.AsyncClientV2(api_key=cohere_api_key)
            logger.info("Cohere reranking enabled")
        else:
            logger.warning("Cohere reranking disabled (no API key or library not installed)")

    async def retrieve(
        self,
        query: str,
        accessible_stage_ids: Optional[List[str]] = None,
        top_k: Optional[int] = None,
        use_reranking: bool = True,
    ) -> List[RetrievalResult]:
        """
        Retrieve relevant content chunks with optional reranking (FR-130, FR-131).

        Args:
            query: User query
            accessible_stage_ids: Stage IDs user can access (FR-078)
            top_k: Number of results to return (after reranking)
            use_reranking: Whether to use Cohere reranking

        Returns:
            Ranked list of retrieval results
        """
        # Get retrieval count (before reranking)
        initial_top_k = self.config.top_k
        final_top_k = top_k or self.config.rerank_top_k

        # Step 1: Semantic search (FR-071)
        logger.info(f"Performing semantic search for query: {query[:50]}...")
        query_embedding = await self.llm_client.create_embedding(query)

        results = await self.vector_store.search(
            query_vector=query_embedding,
            limit=initial_top_k,
            stage_filter=accessible_stage_ids,
            min_score=self.config.min_score,
        )

        if not results:
            logger.info("No results found in semantic search")
            return []

        logger.info(f"Retrieved {len(results)} initial results from vector search")

        # Step 2: Rerank with Cohere (FR-131)
        if use_reranking and self.cohere_client and len(results) > 1:
            try:
                results = await self._rerank_results(query, results, final_top_k)
                logger.info(f"Reranked to top {len(results)} results")
            except Exception as e:
                logger.error(f"Reranking failed: {e}. Using original results.")

        # Return top-k results
        return results[:final_top_k]

    async def _rerank_results(
        self,
        query: str,
        results: List[RetrievalResult],
        top_n: int,
    ) -> List[RetrievalResult]:
        """
        Rerank results using Cohere rerank API (FR-131).

        Based on latest Cohere Python SDK patterns from Context7.

        Args:
            query: User query
            results: Initial retrieval results
            top_n: Number of top results to return

        Returns:
            Reranked results
        """
        # Prepare documents for reranking
        documents = [result.text for result in results]

        # Call Cohere rerank API (Context7 pattern)
        response = await self.cohere_client.rerank(
            model="rerank-v3.5",
            query=query,
            documents=documents,
            top_n=min(top_n, len(documents)),
            return_documents=False,  # We already have the documents
        )

        # Map reranked results back to original results
        reranked = []
        for rerank_result in response.results:
            original_result = results[rerank_result.index]
            # Update score with rerank score
            original_result.score = rerank_result.relevance_score
            original_result.metadata["rerank_score"] = rerank_result.relevance_score
            reranked.append(original_result)

        logger.debug(f"Reranked {len(reranked)} results")
        return reranked

    async def retrieve_with_context(
        self,
        query: str,
        accessible_stage_ids: Optional[List[str]] = None,
        selected_text: Optional[str] = None,
    ) -> tuple[List[RetrievalResult], str]:
        """
        Retrieve relevant chunks and format as context for LLM (FR-068).

        Args:
            query: User query
            accessible_stage_ids: Accessible stage IDs
            selected_text: Selected text for context (FR-068)

        Returns:
            Tuple of (results, formatted_context)
        """
        # Enhance query with selected text if provided (FR-068)
        enhanced_query = query
        if selected_text:
            enhanced_query = f"Context: {selected_text}\n\nQuestion: {query}"
            logger.info("Enhanced query with selected text")

        # Retrieve relevant chunks
        results = await self.retrieve(
            query=enhanced_query,
            accessible_stage_ids=accessible_stage_ids,
        )

        # Format context for LLM
        context_parts = []
        for i, result in enumerate(results, 1):
            citation = f"[{result.stage_name}, {result.content_title}]"
            context_parts.append(
                f"Source {i} {citation}:\n{result.text}\n"
            )

        formatted_context = "\n---\n".join(context_parts)

        return results, formatted_context
