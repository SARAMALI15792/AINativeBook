"""
Enhanced Content API Routes
Endpoints for personalized content delivery, variants, summaries, and code execution
"""

from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import structlog

from src.shared.database import get_session as get_db
from src.core.auth.dependencies import get_current_user
from src.core.auth.models import User
from src.core.content.models import Content
from src.core.content.enhanced_models import (
    ContentVariant,
    ContentSummary,
    InteractiveCodeBlock,
    ContentEngagement,
)
from src.ai.personalization.service import PersonalizationService
from src.ai.translation.service import TranslationService
from src.ai.code_execution.service import CodeExecutionService
from src.ai.content.summary_service import SummaryService
from src.ai.shared.llm_client import LLMClient

logger = structlog.get_logger()

router = APIRouter(prefix="/api/v1/enhanced-content", tags=["Enhanced Content"])

# Initialize services (in production, use dependency injection)
llm_client = LLMClient()
personalization_service = PersonalizationService(llm_client)
translation_service = TranslationService(llm_client)
code_execution_service = CodeExecutionService()
summary_service = SummaryService(llm_client)


@router.get("/{content_id}")
async def get_content(
    content_id: str,
    personalized: bool = Query(default=False, description="Return personalized variant"),
    language: Optional[str] = Query(default=None, description="Language code (en, ur)"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Get content with optional personalization
    Returns appropriate variant based on user preferences
    """
    try:
        # Get base content
        result = await db.execute(
            select(Content).where(Content.id == content_id)
        )
        content = result.scalar_one_or_none()

        if not content:
            raise HTTPException(status_code=404, detail="Content not found")

        # Get personalized variant if requested
        if personalized:
            variant = await personalization_service.get_personalized_content(
                content_id=content_id,
                user_id=str(current_user.id),
                db=db,
            )
        else:
            # Get default variant
            variant_result = await db.execute(
                select(ContentVariant).where(
                    ContentVariant.content_id == content_id,
                    ContentVariant.language_code == language or "en",
                )
            )
            variant = variant_result.scalar_one_or_none()

        # Get summary
        summary_result = await db.execute(
            select(ContentSummary).where(
                ContentSummary.content_id == content_id,
                ContentSummary.language_code == language or "en",
            )
        )
        summary = summary_result.scalar_one_or_none()

        # Get interactive code blocks
        code_blocks_result = await db.execute(
            select(InteractiveCodeBlock)
            .where(InteractiveCodeBlock.content_id == content_id)
            .order_by(InteractiveCodeBlock.order_index)
        )
        code_blocks = code_blocks_result.scalars().all()

        return {
            "content": {
                "id": content.id,
                "title": content.title,
                "description": content.description,
                "difficulty_level": content.difficulty_level,
                "estimated_reading_time": content.estimated_reading_time,
                "tags": content.tags,
                "has_summary": content.has_summary,
                "has_interactive_code": content.has_interactive_code,
            },
            "variant": {
                "id": variant.id if variant else None,
                "variant_type": variant.variant_type if variant else None,
                "language_code": variant.language_code if variant else "en",
                "complexity_level": variant.complexity_level if variant else None,
                "content_json": variant.content_json if variant else {},
                "word_count": variant.word_count if variant else 0,
            } if variant else None,
            "summary": {
                "summary_text": summary.summary_text if summary else None,
                "key_concepts": summary.key_concepts if summary else [],
                "learning_objectives": summary.learning_objectives if summary else [],
                "prerequisites": summary.prerequisites if summary else [],
            } if summary else None,
            "code_blocks": [
                {
                    "id": block.id,
                    "language": block.code_language,
                    "code": block.code_content,
                    "is_editable": block.is_editable,
                    "is_executable": block.is_executable,
                    "title": block.title,
                    "description": block.description,
                }
                for block in code_blocks
            ],
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error("get_content_error", error=str(e), content_id=content_id)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{content_id}/variants")
async def list_content_variants(
    content_id: str,
    db: AsyncSession = Depends(get_db),
):
    """
    List all available variants for content
    (simplified/standard/advanced, en/ur)
    """
    try:
        result = await db.execute(
            select(ContentVariant).where(ContentVariant.content_id == content_id)
        )
        variants = result.scalars().all()

        return {
            "content_id": content_id,
            "variants": [
                {
                    "id": v.id,
                    "variant_type": v.variant_type,
                    "language_code": v.language_code,
                    "complexity_level": v.complexity_level,
                    "word_count": v.word_count,
                    "estimated_reading_time": v.estimated_reading_time,
                }
                for v in variants
            ],
        }

    except Exception as e:
        logger.error("list_variants_error", error=str(e))
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/{content_id}/personalize")
async def trigger_personalization(
    content_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Trigger on-demand personalization for specific content
    Generates personalized variant if not exists
    """
    try:
        variant = await personalization_service.get_personalized_content(
            content_id=content_id,
            user_id=str(current_user.id),
            db=db,
        )

        if not variant:
            raise HTTPException(
                status_code=404,
                detail="Could not generate personalized variant",
            )

        return {
            "message": "Personalization completed",
            "variant_id": variant.id,
            "complexity_level": variant.complexity_level,
            "language_code": variant.language_code,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error("personalization_error", error=str(e))
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/code/execute")
async def execute_code(
    code: str,
    language: str,
    environment: str = "pyodide",
    timeout: Optional[int] = None,
    current_user: User = Depends(get_current_user),
):
    """
    Execute code in sandboxed environment
    Returns output, error, execution time, and status
    """
    try:
        result = await code_execution_service.execute_code(
            code=code,
            language=language,
            environment=environment,
            timeout=timeout,
        )

        logger.info(
            "code_executed",
            user_id=str(current_user.id),
            language=language,
            status=result["status"],
        )

        return result

    except Exception as e:
        logger.error("code_execution_error", error=str(e))
        raise HTTPException(status_code=500, detail="Code execution failed")


@router.post("/code/validate")
async def validate_code(
    code: str,
    language: str,
    current_user: User = Depends(get_current_user),
):
    """
    Validate code without execution
    Checks for syntax errors and security violations
    """
    try:
        result = await code_execution_service.validate_code(
            code=code,
            language=language,
        )

        return result

    except Exception as e:
        logger.error("code_validation_error", error=str(e))
        raise HTTPException(status_code=500, detail="Code validation failed")


@router.post("/{content_id}/track-engagement")
async def track_engagement(
    content_id: str,
    session_id: str,
    time_spent_seconds: int = 0,
    scroll_depth_percent: int = 0,
    code_blocks_executed: int = 0,
    exercises_completed: int = 0,
    summary_viewed: bool = False,
    completed: bool = False,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Track user engagement with content
    Used for analytics and effectiveness metrics
    """
    try:
        # Find or create engagement record
        result = await db.execute(
            select(ContentEngagement).where(
                ContentEngagement.user_id == str(current_user.id),
                ContentEngagement.content_id == content_id,
                ContentEngagement.session_id == session_id,
            )
        )
        engagement = result.scalar_one_or_none()

        if engagement:
            # Update existing
            engagement.time_spent_seconds = time_spent_seconds
            engagement.scroll_depth_percent = scroll_depth_percent
            engagement.code_blocks_executed = code_blocks_executed
            engagement.exercises_completed = exercises_completed
            engagement.summary_viewed = summary_viewed
            engagement.completed = completed
        else:
            # Create new
            engagement = ContentEngagement(
                user_id=str(current_user.id),
                content_id=content_id,
                session_id=session_id,
                time_spent_seconds=time_spent_seconds,
                scroll_depth_percent=scroll_depth_percent,
                code_blocks_executed=code_blocks_executed,
                exercises_completed=exercises_completed,
                summary_viewed=summary_viewed,
                completed=completed,
            )
            db.add(engagement)

        await db.commit()

        return {"message": "Engagement tracked successfully"}

    except Exception as e:
        logger.error("track_engagement_error", error=str(e))
        await db.rollback()
        raise HTTPException(status_code=500, detail="Failed to track engagement")
