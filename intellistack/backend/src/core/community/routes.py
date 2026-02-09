"""Community management API routes (FR-053 to FR-058)."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth.models import User
from src.core.auth.routes import get_current_active_user
from src.core.community import service
from src.core.community.schemas import (
    ForumThreadCreate,
    ForumThreadUpdate,
    ForumThreadResponse,
    ForumPostCreate,
    ForumPostResponse,
    StudyGroupCreate,
    StudyGroupResponse,
    MentorshipResponse,
    ModerationActionCreate,
)
from src.shared.database import get_session

router = APIRouter(prefix="/community", tags=["community"])


# ============================================================================
# Forum Routes (FR-053)
# ============================================================================


@router.get("/forums/categories")
async def get_forum_categories(db: Annotated[AsyncSession, Depends(get_session)]):
    """Get all forum categories."""
    categories = await service.get_forum_categories(db)
    return {"categories": categories}


@router.get("/forums/threads")
async def list_forum_threads(
    category_id: Annotated[str, Query()] = None,
    stage_id: Annotated[str, Query()] = None,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    db: Annotated[AsyncSession, Depends(get_session)] = None,
):
    """
    List forum threads with optional filtering.

    - **category_id**: Filter by category
    - **stage_id**: Filter by stage
    """
    threads, total = await service.get_forum_threads(
        db, category_id=category_id, stage_id=stage_id, skip=skip, limit=limit
    )
    return {
        "threads": [
            {
                "id": t.id,
                "category_id": t.category_id,
                "title": t.title,
                "author_id": t.author_id,
                "reply_count": t.reply_count,
                "view_count": t.view_count,
                "is_pinned": t.is_pinned,
                "created_at": t.created_at.isoformat(),
            }
            for t in threads
        ],
        "total": total,
        "skip": skip,
        "limit": limit,
    }


@router.post("/forums/threads", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_forum_thread(
    thread_data: ForumThreadCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
):
    """
    Create new forum thread (FR-053).

    Students can start discussions in any category.
    """
    thread = await service.create_forum_thread(db, thread_data, str(current_user.id))
    await db.commit()
    return {
        "id": thread.id,
        "title": thread.title,
        "status": thread.status,
        "created_at": thread.created_at.isoformat(),
    }


@router.get("/forums/threads/{thread_id}")
async def get_forum_thread(
    thread_id: str,
    db: Annotated[AsyncSession, Depends(get_session)],
):
    """Get forum thread with details."""
    thread = await service.get_forum_thread(db, thread_id)
    await db.commit()  # Update view count
    return {
        "id": thread.id,
        "category_id": thread.category_id,
        "title": thread.title,
        "content": thread.content,
        "author_id": thread.author_id,
        "reply_count": thread.reply_count,
        "view_count": thread.view_count,
        "is_pinned": thread.is_pinned,
        "is_locked": thread.is_locked,
        "created_at": thread.created_at.isoformat(),
    }


@router.put("/forums/threads/{thread_id}")
async def update_forum_thread(
    thread_id: str,
    thread_data: ForumThreadUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
):
    """Update forum thread (author only)."""
    thread = await service.update_forum_thread(db, thread_id, thread_data, str(current_user.id))
    await db.commit()
    return {"id": thread.id, "status": "updated"}


@router.post("/forums/threads/{thread_id}/posts", status_code=status.HTTP_201_CREATED)
async def create_forum_post(
    thread_id: str,
    post_data: ForumPostCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
):
    """
    Create forum post/reply (FR-053).

    Reply to thread or parent post for nested discussions.
    """
    post_data.thread_id = thread_id
    post = await service.create_forum_post(db, post_data, str(current_user.id))
    await db.commit()
    return {
        "id": post.id,
        "thread_id": post.thread_id,
        "content": post.content,
        "created_at": post.created_at.isoformat(),
    }


@router.get("/forums/threads/{thread_id}/posts")
async def list_forum_posts(
    thread_id: str,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    db: Annotated[AsyncSession, Depends(get_session)] = None,
):
    """List posts in thread."""
    posts, total = await service.get_forum_posts(db, thread_id, skip=skip, limit=limit)
    return {
        "posts": [
            {
                "id": p.id,
                "author_id": p.author_id,
                "content": p.content,
                "is_answer": p.is_answer,
                "created_at": p.created_at.isoformat(),
            }
            for p in posts
        ],
        "total": total,
    }


# ============================================================================
# Study Group Routes (FR-054)
# ============================================================================


@router.post("/study-groups", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_study_group(
    group_data: StudyGroupCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
):
    """
    Create study group (FR-054).

    Students form groups to collaborate on content.
    """
    group = await service.create_study_group(db, group_data, str(current_user.id))
    await db.commit()
    return {
        "id": group.id,
        "name": group.name,
        "max_members": group.max_members,
        "creator_id": group.creator_id,
        "created_at": group.created_at.isoformat(),
    }


@router.get("/study-groups")
async def list_study_groups(
    stage_id: Annotated[str, Query()] = None,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    db: Annotated[AsyncSession, Depends(get_session)] = None,
):
    """
    List study groups with optional stage filter.

    Shows active groups that are open to new members.
    """
    groups, total = await service.get_study_groups(
        db, stage_id=stage_id, skip=skip, limit=limit
    )
    return {
        "groups": [
            {
                "id": g.id,
                "name": g.name,
                "description": g.description,
                "stage_id": g.stage_id,
                "max_members": g.max_members,
                "created_at": g.created_at.isoformat(),
            }
            for g in groups
        ],
        "total": total,
    }


@router.post("/study-groups/{group_id}/join", status_code=status.HTTP_200_OK)
async def join_study_group(
    group_id: str,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
):
    """
    Join study group (FR-054).

    Request to join an open group.
    """
    member = await service.join_study_group(db, group_id, str(current_user.id))
    await db.commit()
    return {
        "group_id": group_id,
        "user_id": str(current_user.id),
        "role": member.role,
        "joined_at": member.joined_at.isoformat(),
    }


# ============================================================================
# Mentorship Routes (FR-055)
# ============================================================================


@router.get("/mentorship/find-mentors")
async def find_mentors(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
):
    """
    Find compatible mentors (FR-055).

    Returns ranked list of potential mentors based on compatibility.
    """
    mentors = await service.find_mentors(db, str(current_user.id))
    return {
        "mentors": [
            {"user_id": mentor_id, "compatibility_score": score}
            for mentor_id, score in mentors
        ]
    }


@router.post("/mentorship", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_mentorship(
    mentor_id: str,
    compatibility_score: float = 0.0,
    current_user: Annotated[User, Depends(get_current_active_user)] = None,
    db: Annotated[AsyncSession, Depends(get_session)] = None,
):
    """
    Create mentorship relationship (FR-055).

    Mentee requests mentorship from mentor.
    """
    mentorship = await service.create_mentorship(
        db,
        mentor_id=mentor_id,
        mentee_id=str(current_user.id),
        compatibility_score=compatibility_score,
    )
    await db.commit()
    return {
        "id": mentorship.id,
        "mentor_id": mentorship.mentor_id,
        "mentee_id": mentorship.mentee_id,
        "status": mentorship.status,
        "started_at": mentorship.started_at.isoformat(),
    }


# ============================================================================
# Moderation Routes (FR-056)
# ============================================================================


@router.post("/moderation/actions", status_code=status.HTTP_201_CREATED)
async def create_moderation_action(
    action_data: ModerationActionCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
):
    """
    Create moderation action (FR-056).

    Moderators flag, review, or remove inappropriate content.
    """
    # TODO: Check moderator role
    record = await service.create_moderation_action(
        db, action_data, str(current_user.id)
    )
    await db.commit()
    return {
        "id": record.id,
        "action": record.action,
        "reason": record.reason,
        "created_at": record.created_at.isoformat(),
    }
