"""Pydantic schemas for RAG system."""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class ContentChunk(BaseModel):
    """Content chunk for vector storage (FR-130)."""

    chunk_id: str
    content_id: str
    stage_id: str
    stage_name: str
    content_title: str
    chunk_index: int
    text: str
    tokens: int
    metadata: dict = Field(default_factory=dict)


class RetrievalResult(BaseModel):
    """Retrieved content chunk with score."""

    chunk_id: str
    content_id: str
    stage_id: str
    stage_name: str
    content_title: str
    text: str
    score: float
    metadata: dict = Field(default_factory=dict)


class RAGQueryRequest(BaseModel):
    """RAG query request (FR-066)."""

    query: str = Field(..., min_length=1, max_length=1000)
    conversation_id: Optional[str] = None
    user_id: str
    selected_text: Optional[str] = None  # For text selection queries (FR-068)


class RAGQueryResponse(BaseModel):
    """RAG query response with citations (FR-067, FR-132)."""

    answer: str
    sources: List[dict] = Field(default_factory=list)
    confidence: float = Field(ge=0.0, le=1.0)
    conversation_id: str
    message_id: str
    retrieved_chunks: int


class StreamChunk(BaseModel):
    """Streaming response chunk (FR-069)."""

    content: str
    is_final: bool = False
    sources: List[dict] = Field(default_factory=list)
    message_id: Optional[str] = None


class ConversationCreate(BaseModel):
    """Create new RAG conversation (FR-070)."""

    user_id: str
    title: Optional[str] = None


class MessageCreate(BaseModel):
    """Create message in conversation (FR-070, FR-074)."""

    conversation_id: str
    user_id: str
    query: str
    selected_text: Optional[str] = None


class SourcePassage(BaseModel):
    """Source passage for citation (FR-075)."""

    stage_name: str
    content_title: str
    text: str
    relevance_score: float
    url: Optional[str] = None
