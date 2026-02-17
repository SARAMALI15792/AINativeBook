"""
Translation Routes
API endpoints for content translation and language management
Sprint 4: Multilingual Support
"""

from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
import structlog

from src.shared.database import get_db
from src.core.auth.dependencies import get_current_user
from src.core.auth.models import User
from src.core.content.models import Content
from src.ai.translation.service import TranslationService
from src.ai.shared.llm_client import LLMClient

logger = structlog.get_logger()

router = APIRouter(prefix="/api/v1/translation", tags=["Translation"])

# Initialize services
llm_client = LLMClient()
translation_service = TranslationService(llm_client)


class TranslateContentRequest(BaseModel):
    """Request to translate content"""
    content_id: str
    target_language: str
    content_type: str = "chapter"
    context: Optional[str] = None


class TranslateTextRequest(BaseModel):
    """Request to translate arbitrary text"""
    text: str
    source_language: str = "en"
    target_language: str = "ur"
    context: Optional[str] = None


class BatchTranslateRequest(BaseModel):
    """Request to batch translate multiple content items"""
    content_ids: List[str]
    target_language: str


class TranslationResponse(BaseModel):
    """Translation response"""
    original_text: str
    translated_text: str
    source_language: str
    target_language: str
    cached: bool
    translation_model: str


@router.post("/content", response_model=TranslationResponse)
async def translate_content(
    request: TranslateContentRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Translate content to target language
    Uses GPT-4 with caching for performance
    """
    try:
        # Get content
        result = await db.execute(
            select(Content).where(Content.id == request.content_id)
        )
        content = result.scalar_one_or_none()

        if not content:
            raise HTTPException(status_code=404, detail="Content not found")

        # Get content text (from description or fetch from file)
        content_text = content.description or "Content text placeholder"

        # Check cache first
        from src.ai.personalization.models import TranslationCache
        cache_result = await db.execute(
            select(TranslationCache).where(
                TranslationCache.content_id == request.content_id,
                TranslationCache.source_language == "en",
                TranslationCache.target_language == request.target_language,
            )
        )
        cached = cache_result.scalar_one_or_none()

        if cached:
            logger.info(
                "translation_cache_hit",
                content_id=request.content_id,
                target_language=request.target_language,
            )
            return TranslationResponse(
                original_text=cached.original_text,
                translated_text=cached.translated_text,
                source_language=cached.source_language,
                target_language=cached.target_language,
                cached=True,
                translation_model=cached.translation_model or "gpt-4",
            )

        # Translate
        translated_text = await translation_service.translate_content(
            content_id=request.content_id,
            content_text=content_text,
            source_language="en",
            target_language=request.target_language,
            content_type=request.content_type,
            context=request.context or content.title,
            use_cache=True,
            db=db,
        )

        logger.info(
            "content_translated",
            content_id=request.content_id,
            target_language=request.target_language,
            user_id=str(current_user.id),
        )

        return TranslationResponse(
            original_text=content_text,
            translated_text=translated_text,
            source_language="en",
            target_language=request.target_language,
            cached=False,
            translation_model="gpt-4",
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("translation_error", error=str(e), content_id=request.content_id)
        raise HTTPException(status_code=500, detail="Translation failed")


@router.post("/text", response_model=TranslationResponse)
async def translate_text(
    request: TranslateTextRequest,
    current_user: User = Depends(get_current_user),
):
    """
    Translate arbitrary text
    Useful for UI elements, error messages, etc.
    """
    try:
        translated_text = await translation_service.translate_text(
            text=request.text,
            source_lang=request.source_language,
            target_lang=request.target_language,
            context=request.context,
        )

        logger.info(
            "text_translated",
            source_language=request.source_language,
            target_language=request.target_language,
            text_length=len(request.text),
        )

        return TranslationResponse(
            original_text=request.text,
            translated_text=translated_text,
            source_language=request.source_language,
            target_language=request.target_language,
            cached=False,
            translation_model="gpt-4",
        )

    except Exception as e:
        logger.error("text_translation_error", error=str(e))
        raise HTTPException(status_code=500, detail="Translation failed")


@router.post("/batch")
async def batch_translate(
    request: BatchTranslateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Batch translate multiple content items
    More efficient than individual translations
    """
    try:
        # Get all content items
        result = await db.execute(
            select(Content).where(Content.id.in_(request.content_ids))
        )
        contents = result.scalars().all()

        if not contents:
            raise HTTPException(status_code=404, detail="No content found")

        # Prepare batch items
        batch_items = [
            {
                "id": content.id,
                "text": content.description or "Content placeholder",
                "type": "chapter",
                "context": content.title,
            }
            for content in contents
        ]

        # Batch translate
        results = await translation_service.batch_translate(
            content_items=batch_items,
            target_language=request.target_language,
            db=db,
        )

        logger.info(
            "batch_translation_completed",
            count=len(results),
            target_language=request.target_language,
            user_id=str(current_user.id),
        )

        return {
            "message": f"Translated {len(results)} items",
            "target_language": request.target_language,
            "results": results,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error("batch_translation_error", error=str(e))
        raise HTTPException(status_code=500, detail="Batch translation failed")


@router.get("/languages")
async def get_supported_languages():
    """
    Get list of supported languages
    """
    return {
        "languages": [
            {
                "code": "en",
                "name": "English",
                "native_name": "English",
                "direction": "ltr",
            },
            {
                "code": "ur",
                "name": "Urdu",
                "native_name": "اردو",
                "direction": "rtl",
            },
        ],
        "default": "en",
    }


@router.get("/cache/stats")
async def get_cache_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Get translation cache statistics
    Admin only endpoint
    """
    try:
        from src.ai.personalization.models import TranslationCache
        from sqlalchemy import func

        # Total cached translations
        total_result = await db.execute(
            select(func.count(TranslationCache.id))
        )
        total = total_result.scalar()

        # By language
        lang_result = await db.execute(
            select(
                TranslationCache.target_language,
                func.count(TranslationCache.id)
            ).group_by(TranslationCache.target_language)
        )
        by_language = {lang: count for lang, count in lang_result.all()}

        # Cache size (approximate)
        size_result = await db.execute(
            select(func.sum(func.length(TranslationCache.translated_text)))
        )
        total_size = size_result.scalar() or 0

        return {
            "total_cached": total,
            "by_language": by_language,
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
        }

    except Exception as e:
        logger.error("cache_stats_error", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to get cache stats")


@router.delete("/cache/clear")
async def clear_translation_cache(
    language: Optional[str] = Query(None, description="Clear specific language only"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Clear translation cache
    Admin only endpoint
    """
    try:
        from src.ai.personalization.models import TranslationCache

        if language:
            # Clear specific language
            result = await db.execute(
                select(TranslationCache).where(
                    TranslationCache.target_language == language
                )
            )
            items = result.scalars().all()
            for item in items:
                await db.delete(item)

            await db.commit()

            logger.info(
                "cache_cleared",
                language=language,
                count=len(items),
                user_id=str(current_user.id),
            )

            return {
                "message": f"Cleared {len(items)} cached translations for {language}",
                "language": language,
                "count": len(items),
            }
        else:
            # Clear all
            result = await db.execute(select(TranslationCache))
            items = result.scalars().all()
            for item in items:
                await db.delete(item)

            await db.commit()

            logger.info(
                "cache_cleared_all",
                count=len(items),
                user_id=str(current_user.id),
            )

            return {
                "message": f"Cleared all {len(items)} cached translations",
                "count": len(items),
            }

    except Exception as e:
        logger.error("clear_cache_error", error=str(e))
        await db.rollback()
        raise HTTPException(status_code=500, detail="Failed to clear cache")
