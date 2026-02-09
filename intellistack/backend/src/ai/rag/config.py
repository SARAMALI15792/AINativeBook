"""Qdrant collection configuration for RAG system."""

from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class QdrantConfig(BaseSettings):
    """Qdrant configuration (FR-066)."""

    host: str = Field(default="localhost", env="QDRANT_HOST")
    port: int = Field(default=6333, env="QDRANT_PORT")
    api_key: Optional[str] = Field(default=None, env="QDRANT_API_KEY")
    collection_name: str = "intellistack_content"

    # Vector configuration
    vector_size: int = 1536  # text-embedding-3-small dimension
    distance_metric: str = "Cosine"

    # Chunking configuration (FR-130)
    chunk_size: int = 512  # tokens
    chunk_overlap: int = 50  # tokens

    # Retrieval configuration
    top_k: int = 10  # Initial retrieval count
    rerank_top_k: int = 5  # After reranking (FR-131)
    min_score: float = 0.7  # Minimum relevance score

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def get_qdrant_config() -> QdrantConfig:
    """Get Qdrant configuration."""
    return QdrantConfig()
