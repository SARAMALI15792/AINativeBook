"""PostgreSQL-based session storage for AI Tutor conversations.

Replaces SQLiteSession from OpenAI Agents SDK with PostgreSQL-backed storage.
This aligns with the project's PostgreSQL-only database strategy.
"""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy import Column, DateTime, ForeignKey, Index, String, Text, select, delete
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.database import Base
from src.config.logging import get_logger

logger = get_logger(__name__)


class TutorSessionItem(Base):
    """Individual message/item in a tutor conversation session.

    Stores conversation history for AI Tutor sessions, replacing SQLiteSession
    from the OpenAI Agents SDK with PostgreSQL-backed persistence.
    """
    __tablename__ = "tutor_session_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(String(255), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    role = Column(String(50), nullable=False)  # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    item_metadata = Column("metadata", JSONB, default=dict)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    __table_args__ = (
        Index('idx_tutor_session_items_session_id_created', 'session_id', 'created_at'),
    )


class PostgresSession:
    """PostgreSQL-based session storage for AI Tutor conversations.

    Compatible interface replacement for OpenAI Agents SDK's SQLiteSession.
    Maintains conversation context across multiple turns using PostgreSQL.

    Args:
        session_id: Unique identifier for the conversation session
        db_session: SQLAlchemy async session for database operations
    """

    def __init__(self, session_id: str, db_session: AsyncSession, user_id: Optional[uuid.UUID] = None):
        self.session_id = session_id
        self.db = db_session
        self.user_id = user_id
        self._items_cache: Optional[List[Dict[str, Any]]] = None

    async def get_items(self) -> List[Dict[str, Any]]:
        """Get all items in this session, ordered by creation time.

        Returns:
            List of session items with role, content, and metadata.
        """
        if self._items_cache is None:
            result = await self.db.execute(
                select(TutorSessionItem)
                .where(TutorSessionItem.session_id == self.session_id)
                .order_by(TutorSessionItem.created_at)
            )
            items = result.scalars().all()
            self._items_cache = [
                {
                    "id": str(item.id),
                    "role": item.role,
                    "content": item.content,
                    "metadata": item.item_metadata or {},
                    "created_at": item.created_at.isoformat() if item.created_at else None,
                }
                for item in items
            ]
            logger.debug(f"Loaded {len(self._items_cache)} items for session {self.session_id}")
        return self._items_cache

    async def add_item(self, role: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Add an item to the session.

        Args:
            role: The role ('user' or 'assistant')
            content: The message content
            metadata: Optional metadata dictionary
        """
        item = TutorSessionItem(
            session_id=self.session_id,
            user_id=self.user_id,
            role=role,
            content=content,
            item_metadata=metadata or {},
        )
        self.db.add(item)
        await self.db.commit()
        await self.db.refresh(item)
        self._items_cache = None  # Invalidate cache
        logger.debug(f"Added item to session {self.session_id}: {role}")

    async def clear(self) -> None:
        """Clear all items in this session."""
        result = await self.db.execute(
            delete(TutorSessionItem).where(TutorSessionItem.session_id == self.session_id)
        )
        await self.db.commit()
        self._items_cache = []
        logger.info(f"Cleared session {self.session_id}: {result.rowcount} items deleted")

    async def get_conversation_history(self, limit: Optional[int] = None) -> List[Dict[str, str]]:
        """Get conversation history formatted for LLM context.

        Args:
            limit: Maximum number of recent turns to include (None for all)

        Returns:
            List of messages with 'role' and 'content' keys.
        """
        items = await self.get_items()

        messages = []
        for item in items:
            messages.append({
                "role": item["role"],
                "content": item["content"],
            })

        if limit and len(messages) > limit:
            # Keep system message if present, then take last 'limit' messages
            messages = messages[-limit:]

        return messages

    async def get_turn_count(self) -> int:
        """Get the number of conversation turns (user messages).

        Returns:
            Number of user messages in the session.
        """
        items = await self.get_items()
        return len([i for i in items if i["role"] == "user"])
