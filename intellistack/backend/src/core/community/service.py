"""Community management service (FR-053 to FR-058)."""

import logging
from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy import select, func, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status

from src.core.community.models import (
    ForumCategory,
    ForumThread,
    ForumPost,
    StudyGroup,
    StudyGroupMember,
    Mentorship,
    ModerationRecord,
    ModerationAction,
    PostStatus,
)
from src.core.community.schemas import (
    ForumThreadCreate,
    ForumThreadUpdate,
    ForumPostCreate,
    StudyGroupCreate,
    ModerationActionCreate,
)
from src.core.learning.models import Progress

logger = logging.getLogger(__name__)


# ============================================================================
# Forum Management (FR-053)
# ============================================================================


async def get_forum_categories(db: AsyncSession) -> List[ForumCategory]:
    """Get all forum categories ordered by index."""
    result = await db.execute(
        select(ForumCategory).order_by(ForumCategory.order_index)
    )
    return result.scalars().all()


async def get_forum_threads(
    db: AsyncSession,
    category_id: Optional[str] = None,
    stage_id: Optional[str] = None,
    skip: int = 0,
    limit: int = 20,
) -> tuple[List[ForumThread], int]:
    """Get forum threads with optional filtering."""
    query = select(ForumThread).where(ForumThread.status == PostStatus.PUBLISHED)

    if category_id:
        query = query.where(ForumThread.category_id == category_id)
    if stage_id:
        query = query.where(ForumThread.stage_id == stage_id)

    # Count total
    count_result = await db.execute(select(func.count(ForumThread.id)).where(
        (ForumThread.status == PostStatus.PUBLISHED) &
        (ForumThread.category_id == category_id if category_id else True) &
        (ForumThread.stage_id == stage_id if stage_id else True)
    ))
    total = count_result.scalar()

    # Get paginated results
    result = await db.execute(
        query.order_by(ForumThread.is_pinned.desc(), ForumThread.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    threads = result.scalars().all()
    return threads, total


async def create_forum_thread(
    db: AsyncSession,
    thread_data: ForumThreadCreate,
    user_id: str,
) -> ForumThread:
    """Create new forum thread (FR-053)."""
    # Verify category exists
    category = await db.get(ForumCategory, thread_data.category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    thread = ForumThread(
        category_id=thread_data.category_id,
        author_id=user_id,
        title=thread_data.title,
        content=thread_data.content,
        stage_id=thread_data.stage_id,
        status=PostStatus.DRAFT if category.requires_approval else PostStatus.PUBLISHED,
    )

    db.add(thread)
    await db.flush()
    return thread


async def get_forum_thread(db: AsyncSession, thread_id: str) -> ForumThread:
    """Get forum thread with posts."""
    thread = await db.get(ForumThread, thread_id)
    if not thread:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Thread not found")

    # Increment view count
    thread.view_count += 1
    db.add(thread)

    return thread


async def update_forum_thread(
    db: AsyncSession,
    thread_id: str,
    thread_data: ForumThreadUpdate,
    user_id: str,
) -> ForumThread:
    """Update forum thread (author or moderator only)."""
    thread = await db.get(ForumThread, thread_id)
    if not thread:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Thread not found")

    if thread.author_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only thread author can edit",
        )

    if thread_data.title:
        thread.title = thread_data.title
    if thread_data.content:
        thread.content = thread_data.content
    if thread_data.is_pinned is not None:
        thread.is_pinned = thread_data.is_pinned
    if thread_data.is_locked is not None:
        thread.is_locked = thread_data.is_locked

    db.add(thread)
    return thread


async def create_forum_post(
    db: AsyncSession,
    post_data: ForumPostCreate,
    user_id: str,
) -> ForumPost:
    """Create forum post/reply (FR-053)."""
    thread = await db.get(ForumThread, post_data.thread_id)
    if not thread:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Thread not found")

    if thread.is_locked:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Thread is locked",
        )

    post = ForumPost(
        thread_id=post_data.thread_id,
        parent_post_id=post_data.parent_post_id,
        author_id=user_id,
        content=post_data.content,
        status=PostStatus.PUBLISHED,
    )

    db.add(post)
    thread.reply_count += 1
    thread.last_activity_at = datetime.now(timezone.utc)
    db.add(thread)

    return post


async def get_forum_posts(
    db: AsyncSession,
    thread_id: str,
    skip: int = 0,
    limit: int = 50,
) -> tuple[List[ForumPost], int]:
    """Get posts in a thread."""
    query = select(ForumPost).where(
        (ForumPost.thread_id == thread_id) & (ForumPost.status == PostStatus.PUBLISHED)
    )

    count_result = await db.execute(
        select(func.count(ForumPost.id)).where(
            (ForumPost.thread_id == thread_id) & (ForumPost.status == PostStatus.PUBLISHED)
        )
    )
    total = count_result.scalar()

    result = await db.execute(
        query.order_by(ForumPost.created_at).offset(skip).limit(limit)
    )
    posts = result.scalars().all()
    return posts, total


# ============================================================================
# Study Groups (FR-054)
# ============================================================================


async def create_study_group(
    db: AsyncSession,
    group_data: StudyGroupCreate,
    user_id: str,
) -> StudyGroup:
    """Create study group."""
    group = StudyGroup(
        creator_id=user_id,
        name=group_data.name,
        description=group_data.description,
        stage_id=group_data.stage_id,
        max_members=group_data.max_members,
    )

    db.add(group)
    await db.flush()

    # Add creator as member
    member = StudyGroupMember(study_group_id=group.id, user_id=user_id, role="moderator")
    db.add(member)

    return group


async def join_study_group(
    db: AsyncSession,
    group_id: str,
    user_id: str,
) -> StudyGroupMember:
    """Join study group (FR-054)."""
    group = await db.get(StudyGroup, group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")

    if not group.is_open:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Group is closed",
        )

    # Check member limit
    member_count_result = await db.execute(
        select(func.count(StudyGroupMember.id)).where(
            (StudyGroupMember.study_group_id == group_id) & (StudyGroupMember.left_at == None)
        )
    )
    member_count = member_count_result.scalar()

    if member_count >= group.max_members:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Group is full",
        )

    # Check if already member
    existing = await db.execute(
        select(StudyGroupMember).where(
            (StudyGroupMember.study_group_id == group_id)
            & (StudyGroupMember.user_id == user_id)
            & (StudyGroupMember.left_at == None)
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Already member of group",
        )

    member = StudyGroupMember(study_group_id=group_id, user_id=user_id, role="member")
    db.add(member)

    return member


async def get_study_groups(
    db: AsyncSession,
    stage_id: Optional[str] = None,
    skip: int = 0,
    limit: int = 20,
) -> tuple[List[StudyGroup], int]:
    """Get study groups."""
    query = select(StudyGroup).where(StudyGroup.is_open == True)

    if stage_id:
        query = query.where(StudyGroup.stage_id == stage_id)

    count_result = await db.execute(
        select(func.count(StudyGroup.id)).where(StudyGroup.is_open == True)
    )
    total = count_result.scalar()

    result = await db.execute(query.order_by(StudyGroup.created_at.desc()).offset(skip).limit(limit))
    groups = result.scalars().all()

    return groups, total


# ============================================================================
# Mentorship Matching (FR-055)
# ============================================================================


async def find_mentors(
    db: AsyncSession,
    mentee_id: str,
    stage_id: Optional[str] = None,
) -> List[tuple]:
    """Find compatible mentors for a mentee."""
    # Get mentee's progress
    mentee_progress = await db.execute(
        select(Progress).where(Progress.user_id == mentee_id)
    )
    mentee_prog = mentee_progress.scalar_one_or_none()

    if not mentee_prog:
        return []

    # Find mentors ahead in their learning (at least 1 stage ahead)
    query = select(Progress).where(
        (Progress.stage_id > mentee_prog.stage_id) if mentee_prog.stage_id else True
    )

    result = await db.execute(query)
    potential_mentors = result.scalars().all()

    # Score compatibility (simplified - can be enhanced with interests, availability, etc.)
    scored_mentors = []
    for mentor_prog in potential_mentors:
        if mentor_prog.user_id == mentee_id:
            continue

        # Check if mentorship already exists
        existing = await db.execute(
            select(Mentorship).where(
                (Mentorship.mentor_id == mentor_prog.user_id)
                & (Mentorship.mentee_id == mentee_id)
                & (Mentorship.status == "active")
            )
        )
        if existing.scalar_one_or_none():
            continue

        # Simple compatibility score: stage difference + completion percentage
        stage_diff = (mentor_prog.stage_id or 0) - (mentee_prog.stage_id or 0)
        score = min(100, (stage_diff * 20) + mentor_prog.completion_percentage)

        scored_mentors.append((mentor_prog.user_id, score))

    # Sort by score descending
    scored_mentors.sort(key=lambda x: x[1], reverse=True)
    return scored_mentors[:10]  # Return top 10


async def create_mentorship(
    db: AsyncSession,
    mentor_id: str,
    mentee_id: str,
    stage_id: Optional[str] = None,
    compatibility_score: float = 0.0,
) -> Mentorship:
    """Create mentorship relationship (FR-055)."""
    # Check if relationship already exists
    existing = await db.execute(
        select(Mentorship).where(
            (Mentorship.mentor_id == mentor_id)
            & (Mentorship.mentee_id == mentee_id)
            & (Mentorship.status == "active")
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Mentorship already exists",
        )

    mentorship = Mentorship(
        mentor_id=mentor_id,
        mentee_id=mentee_id,
        stage_id=stage_id,
        compatibility_score=compatibility_score,
        status="active",
    )

    db.add(mentorship)
    return mentorship


# ============================================================================
# Moderation (FR-056)
# ============================================================================


async def create_moderation_action(
    db: AsyncSession,
    action_data: ModerationActionCreate,
    moderator_id: str,
) -> ModerationRecord:
    """Create moderation action (FR-056)."""
    record = ModerationRecord(
        moderator_id=moderator_id,
        user_id=action_data.user_id,
        thread_id=action_data.thread_id,
        post_id=action_data.post_id,
        action=action_data.action,
        reason=action_data.reason,
        status="active",
    )

    db.add(record)

    # Apply action to target
    if action_data.post_id:
        post = await db.get(ForumPost, action_data.post_id)
        if post:
            if action_data.action in [ModerationAction.HIDDEN, ModerationAction.REMOVED]:
                post.status = PostStatus.DELETED
            db.add(post)

    elif action_data.thread_id:
        thread = await db.get(ForumThread, action_data.thread_id)
        if thread:
            if action_data.action in [ModerationAction.HIDDEN, ModerationAction.REMOVED]:
                thread.status = PostStatus.DELETED
            db.add(thread)

    logger.info(
        f"Moderation action: {action_data.action} by {moderator_id}",
        extra={"reason": action_data.reason},
    )

    return record
