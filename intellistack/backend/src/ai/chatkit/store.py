"""
ChatKit Store - PostgreSQL-backed thread and message persistence.

Implements the ChatKit Store interface for thread and message management.
Based on the ChatKit Python SDK patterns.
"""

import uuid
import logging
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any

from sqlalchemy import select, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession

from .models import ChatKitThread, ChatKitThreadItem

logger = logging.getLogger(__name__)


class PostgresChatKitStore:
    """
    ChatKit store implementation backed by PostgreSQL.

    Handles:
    - Thread creation and management
    - Message persistence
    - Thread history retrieval
    - Retention policy enforcement (30 days after enrollment ends)
    """

    def __init__(self, db_session: AsyncSession):
        """
        Initialize store with database session.

        Args:
            db_session: SQLAlchemy async session
        """
        self.db = db_session

    async def create_thread(
        self,
        user_id: str,
        metadata: Optional[Dict[str, Any]] = None,
        course_id: Optional[str] = None,
        lesson_stage: Optional[int] = None,
    ) -> ChatKitThread:
        """
        Create a new conversation thread.

        Args:
            user_id: ID of the user owning this thread
            metadata: Optional metadata (page context, tags, etc.)
            course_id: Associated course ID
            lesson_stage: Current learning stage (1-5)

        Returns:
            Created thread object
        """
        thread = ChatKitThread(
            id=str(uuid.uuid4()),
            user_id=user_id,
            course_id=course_id,
            lesson_stage=lesson_stage,
            status="active",
            metadata=metadata or {},
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        self.db.add(thread)
        await self.db.commit()
        await self.db.refresh(thread)

        logger.info(f"Created thread {thread.id} for user {user_id}")
        return thread

    async def load_thread(self, thread_id: str) -> Optional[ChatKitThread]:
        """
        Load a thread by ID with its items.

        Args:
            thread_id: Thread ID to load

        Returns:
            Thread object with items, or None if not found
        """
        stmt = select(ChatKitThread).where(ChatKitThread.id == thread_id)
        result = await self.db.execute(stmt)
        thread = result.scalar_one_or_none()

        if thread:
            # Load items eagerly
            await self.db.refresh(thread, ["items"])

        return thread

    async def load_thread_items(
        self,
        thread_id: str,
        limit: int = 50,
        before_id: Optional[str] = None,
    ) -> List[ChatKitThreadItem]:
        """
        Load thread items (messages) with pagination.

        Args:
            thread_id: Thread ID
            limit: Maximum items to return
            before_id: Load items before this ID (for pagination)

        Returns:
            List of thread items ordered by created_at
        """
        stmt = select(ChatKitThreadItem).where(
            ChatKitThreadItem.thread_id == thread_id
        )

        if before_id:
            # Get the created_at of the before item
            before_stmt = select(ChatKitThreadItem.created_at).where(
                ChatKitThreadItem.id == before_id
            )
            before_result = await self.db.execute(before_stmt)
            before_time = before_result.scalar_one_or_none()

            if before_time:
                stmt = stmt.where(ChatKitThreadItem.created_at < before_time)

        stmt = stmt.order_by(ChatKitThreadItem.created_at.desc()).limit(limit)

        result = await self.db.execute(stmt)
        items = result.scalars().all()

        # Return in chronological order
        return list(reversed(items))

    async def save_thread_item(
        self,
        thread_id: str,
        role: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> ChatKitThreadItem:
        """
        Save a message to a thread.

        Args:
            thread_id: Thread ID
            role: Message role ('user' or 'assistant')
            content: Message content
            metadata: Optional metadata (token count, page context, etc.)

        Returns:
            Created thread item
        """
        item = ChatKitThreadItem(
            id=str(uuid.uuid4()),
            thread_id=thread_id,
            role=role,
            content=content,
            metadata=metadata or {},
            created_at=datetime.utcnow(),
        )

        self.db.add(item)

        # Update thread's updated_at timestamp
        thread_stmt = select(ChatKitThread).where(ChatKitThread.id == thread_id)
        result = await self.db.execute(thread_stmt)
        thread = result.scalar_one_or_none()

        if thread:
            thread.updated_at = datetime.utcnow()

            # Auto-generate title from first user message if not set
            if not thread.title and role == "user":
                thread.title = self._generate_title(content)

        await self.db.commit()
        await self.db.refresh(item)

        logger.debug(f"Saved {role} message to thread {thread_id}")
        return item

    async def delete_thread(self, thread_id: str, user_id: str) -> bool:
        """
        Delete a thread and all its items.

        Args:
            thread_id: Thread ID to delete
            user_id: User ID (for authorization)

        Returns:
            True if deleted, False if not found or not authorized
        """
        # Verify ownership
        stmt = select(ChatKitThread).where(
            and_(
                ChatKitThread.id == thread_id,
                ChatKitThread.user_id == user_id,
            )
        )
        result = await self.db.execute(stmt)
        thread = result.scalar_one_or_none()

        if not thread:
            return False

        # Delete thread (cascade deletes items)
        await self.db.delete(thread)
        await self.db.commit()

        logger.info(f"Deleted thread {thread_id}")
        return True

    async def list_threads(
        self,
        user_id: str,
        limit: int = 20,
        offset: int = 0,
        status: Optional[str] = None,
    ) -> List[ChatKitThread]:
        """
        List user's threads ordered by last activity.

        Args:
            user_id: User ID
            limit: Maximum threads to return
            offset: Offset for pagination
            status: Filter by status (active, archived)

        Returns:
            List of threads
        """
        stmt = select(ChatKitThread).where(ChatKitThread.user_id == user_id)

        if status:
            stmt = stmt.where(ChatKitThread.status == status)

        stmt = stmt.order_by(ChatKitThread.updated_at.desc())
        stmt = stmt.offset(offset).limit(limit)

        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def update_thread(
        self,
        thread_id: str,
        user_id: str,
        title: Optional[str] = None,
        status: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Optional[ChatKitThread]:
        """
        Update thread properties.

        Args:
            thread_id: Thread ID
            user_id: User ID (for authorization)
            title: New title
            status: New status (active, archived)
            metadata: Updated metadata (merged with existing)

        Returns:
            Updated thread or None
        """
        stmt = select(ChatKitThread).where(
            and_(
                ChatKitThread.id == thread_id,
                ChatKitThread.user_id == user_id,
            )
        )
        result = await self.db.execute(stmt)
        thread = result.scalar_one_or_none()

        if not thread:
            return None

        if title is not None:
            thread.title = title
        if status is not None:
            thread.status = status
        if metadata is not None:
            thread.metadata = {**thread.metadata, **metadata}

        thread.updated_at = datetime.utcnow()

        await self.db.commit()
        await self.db.refresh(thread)

        return thread

    async def cleanup_expired_threads(
        self,
        retention_days: int = 30,
    ) -> int:
        """
        Delete threads that have exceeded retention period.

        Threads are deleted when enrollment_ended_at + retention_days < now.

        Args:
            retention_days: Days to retain after enrollment ends

        Returns:
            Number of threads deleted
        """
        cutoff_date = datetime.utcnow() - timedelta(days=retention_days)

        stmt = delete(ChatKitThread).where(
            and_(
                ChatKitThread.enrollment_ended_at.isnot(None),
                ChatKitThread.enrollment_ended_at < cutoff_date,
            )
        )

        result = await self.db.execute(stmt)
        await self.db.commit()

        deleted_count = result.rowcount
        logger.info(f"Cleaned up {deleted_count} expired threads")

        return deleted_count

    def _generate_title(self, first_message: str, max_length: int = 50) -> str:
        """
        Generate thread title from first message.

        Args:
            first_message: First user message
            max_length: Maximum title length

        Returns:
            Generated title
        """
        # Clean up message
        title = first_message.strip()

        # Remove common question prefixes
        for prefix in ["How do I", "What is", "Why does", "Can you"]:
            if title.lower().startswith(prefix.lower()):
                title = title[len(prefix):].strip()
                break

        # Truncate if too long
        if len(title) > max_length:
            title = title[:max_length - 3] + "..."

        return title.capitalize() if title else "New conversation"
