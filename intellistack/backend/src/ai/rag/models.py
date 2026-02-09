"""Database models for RAG conversation tracking."""

from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.shared.database import Base


class RAGConversation(Base):
    """
    RAG conversation tracking (FR-070).

    Maintains conversation context across multiple questions.
    """

    __tablename__ = "rag_conversations"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
    )
    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("users.id"), nullable=False, index=True
    )
    title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    messages: Mapped[list["RAGMessage"]] = relationship(
        "RAGMessage", back_populates="conversation", cascade="all, delete-orphan"
    )


class RAGMessage(Base):
    """
    Individual message in RAG conversation (FR-070, FR-074).

    Stores user queries and AI responses with metadata.
    """

    __tablename__ = "rag_messages"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
    )
    conversation_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("rag_conversations.id"), nullable=False, index=True
    )
    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("users.id"), nullable=False, index=True
    )

    # Message content
    role: Mapped[str] = mapped_column(String(20), nullable=False)  # user, assistant
    content: Mapped[str] = mapped_column(Text, nullable=False)
    query: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # Original query
    selected_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # FR-068

    # Response metadata
    confidence: Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # FR-072
    sources: Mapped[dict] = mapped_column(JSONB, default=dict)  # Citations (FR-067)
    retrieved_count: Mapped[int] = mapped_column(Integer, default=0)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationships
    conversation: Mapped["RAGConversation"] = relationship(
        "RAGConversation", back_populates="messages"
    )
    retrievals: Mapped[list["RAGRetrieval"]] = relationship(
        "RAGRetrieval", back_populates="message", cascade="all, delete-orphan"
    )


class RAGRetrieval(Base):
    """
    Track which content chunks were retrieved for each message (FR-079).

    Used for quality improvement and analytics.
    """

    __tablename__ = "rag_retrievals"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
    )
    message_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("rag_messages.id"), nullable=False, index=True
    )

    # Retrieved content metadata
    chunk_id: Mapped[str] = mapped_column(String(255), nullable=False)
    content_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("content_items.id"), nullable=False
    )
    stage_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("stages.id"), nullable=False
    )

    # Retrieval scores
    relevance_score: Mapped[float] = mapped_column(Float, nullable=False)
    rerank_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    was_used_in_response: Mapped[bool] = mapped_column(default=True)

    # Timestamp
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationships
    message: Mapped["RAGMessage"] = relationship("RAGMessage", back_populates="retrievals")
