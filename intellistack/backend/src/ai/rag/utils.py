"""Utility functions for RAG service and stage access control."""

from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.learning.models import Progress, Stage


async def get_user_current_stage_number(db: AsyncSession, user_id: str) -> int:
    """
    Get the user's current stage number based on their progress.

    Args:
        db: Database session
        user_id: User ID

    Returns:
        Current stage number (1-5)
    """
    # Get user's progress record
    result = await db.execute(
        select(Progress).where(Progress.user_id == user_id)
    )
    progress = result.scalar_one_or_none()

    if not progress:
        # New user - only access to Stage 1
        return 1

    # If the progress has a current_stage_id, get the corresponding stage number
    if progress.current_stage_id:
        stage_result = await db.execute(
            select(Stage).where(Stage.id == progress.current_stage_id)
        )
        stage = stage_result.scalar_one_or_none()
        if stage:
            return stage.number

    # Fallback to current_stage or default to 1
    return 1


async def get_accessible_stage_ids(db: AsyncSession, user_id: str) -> List[str]:
    """
    Get stage IDs accessible to user based on their progress.

    Args:
        db: Database session
        user_id: User ID

    Returns:
        List of accessible stage IDs
    """
    current_stage_number = await get_user_current_stage_number(db, user_id)

    # Get all stages up to the user's current stage
    result = await db.execute(
        select(Stage.id).where(Stage.number <= current_stage_number)
    )
    stage_ids = [row[0] for row in result.all()]

    return stage_ids


async def get_stage_number_by_id(db: AsyncSession, stage_id: str) -> int:
    """
    Get stage number by stage ID.

    Args:
        db: Database session
        stage_id: Stage ID

    Returns:
        Stage number
    """
    result = await db.execute(
        select(Stage.number).where(Stage.id == stage_id)
    )
    stage_number = result.scalar_one_or_none()
    return stage_number if stage_number is not None else 1