"""
Translation Service
Handles content translation with caching and quality assurance
Sprint 5: Translation System (Urdu Support)
"""

from typing import Optional, List, Dict, Any
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import structlog
from datetime import datetime, timedelta

from src.ai.personalization.models import TranslationCache
from src.ai.shared.llm_client import LLMClient

logger = structlog.get_logger()


class TranslationService:
    """
    Handles content translation with GPT-4 and caching
    Implements FR-084: Urdu translation toggle
    """

    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client
        self.cache_ttl_days = 30  # Cache translations for 30 days

    async def translate_content(
        self,
        content_id: str,
        content_text: str,
        source_language: str,
        target_language: str,
        content_type: str,
        context: Optional[str] = None,
        use_cache: bool = True,
        db: Optional[AsyncSession] = None,
    ) -> str:
        """
        Translate content to target language
        - Check cache first
        - Use GPT-4 for technical accuracy
        - Preserve code blocks, markdown formatting
        - Cache result

        Args:
            content_id: UUID of content being translated
            content_text: Text to translate
            source_language: Source language code (e.g., 'en')
            target_language: Target language code (e.g., 'ur')
            content_type: Type of content ('chapter', 'exercise', 'quiz_question')
            context: Optional context about the content topic
            use_cache: Whether to use cached translations
            db: Database session for caching

        Returns:
            Translated text
        """
        try:
            # Check cache first
            if use_cache and db:
                cached = await self._get_cached_translation(
                    content_id=content_id,
                    source_language=source_language,
                    target_language=target_language,
                    db=db,
                )
                if cached:
                    logger.info(
                        "translation_cache_hit",
                        content_id=content_id,
                        target_language=target_language,
                    )
                    return cached.translated_text

            # Perform translation
            translated_text = await self._translate_with_llm(
                text=content_text,
                source_lang=source_language,
                target_lang=target_language,
                context=context,
            )

            # Cache the result
            if db:
                await self._cache_translation(
                    content_id=content_id,
                    content_type=content_type,
                    source_language=source_language,
                    target_language=target_language,
                    original_text=content_text,
                    translated_text=translated_text,
                    db=db,
                )

            logger.info(
                "translation_completed",
                content_id=content_id,
                source_language=source_language,
                target_language=target_language,
                original_length=len(content_text),
                translated_length=len(translated_text),
            )

            return translated_text

        except Exception as e:
            logger.error(
                "translation_error",
                error=str(e),
                content_id=content_id,
                target_language=target_language,
            )
            # Return original text as fallback
            return content_text

    async def translate_text(
        self,
        text: str,
        source_lang: str,
        target_lang: str,
        context: Optional[str] = None,
    ) -> str:
        """
        Translate arbitrary text with context
        Context helps with technical term accuracy

        Args:
            text: Text to translate
            source_lang: Source language code
            target_lang: Target language code
            context: Optional context (e.g., "robotics", "machine learning")

        Returns:
            Translated text
        """
        return await self._translate_with_llm(text, source_lang, target_lang, context)

    async def batch_translate(
        self,
        content_items: List[Dict[str, Any]],
        target_language: str,
        db: AsyncSession,
    ) -> List[Dict[str, Any]]:
        """
        Batch translation for efficiency

        Args:
            content_items: List of dicts with 'id', 'text', 'type', 'context'
            target_language: Target language code
            db: Database session

        Returns:
            List of dicts with 'id', 'original_text', 'translated_text'
        """
        results = []

        for item in content_items:
            translated = await self.translate_content(
                content_id=item["id"],
                content_text=item["text"],
                source_language="en",
                target_language=target_language,
                content_type=item.get("type", "chapter"),
                context=item.get("context"),
                use_cache=True,
                db=db,
            )

            results.append(
                {
                    "id": item["id"],
                    "original_text": item["text"],
                    "translated_text": translated,
                }
            )

        logger.info(
            "batch_translation_completed",
            count=len(results),
            target_language=target_language,
        )

        return results

    async def _translate_with_llm(
        self,
        text: str,
        source_lang: str,
        target_lang: str,
        context: Optional[str] = None,
    ) -> str:
        """
        Perform translation using GPT-4
        Optimized for technical robotics content
        """
        # Build translation prompt
        prompt = self._build_translation_prompt(
            text=text,
            source_lang=source_lang,
            target_lang=target_lang,
            context=context,
        )

        # Call LLM
        response = await self.llm_client.generate(
            prompt=prompt,
            temperature=0.3,  # Lower temperature for more consistent translations
            max_tokens=4000,
        )

        return response.strip()

    def _build_translation_prompt(
        self,
        text: str,
        source_lang: str,
        target_lang: str,
        context: Optional[str] = None,
    ) -> str:
        """
        Build translation prompt optimized for technical content
        """
        lang_names = {
            "en": "English",
            "ur": "Urdu",
        }

        source_name = lang_names.get(source_lang, source_lang)
        target_name = lang_names.get(target_lang, target_lang)

        context_info = f"\n\nContext: This content is from a {context} chapter in a Physical AI and Humanoid Robotics course." if context else ""

        prompt = f"""You are translating technical robotics educational content from {source_name} to {target_name}.{context_info}

Requirements:
1. Maintain technical accuracy - robotics terms must be precise
2. Keep code blocks UNCHANGED (do not translate code)
3. Preserve markdown formatting (headers, lists, links, etc.)
4. Use appropriate {target_name} technical terms
5. Keep English terms in parentheses for clarity when needed (e.g., "کرنل (Kernel)")
6. Maintain the educational tone - clear and accessible
7. Preserve any mathematical notation or formulas
8. Keep URLs and file paths unchanged

Original {source_name} text:
{text}

Translate to {target_name}:"""

        return prompt

    async def _get_cached_translation(
        self,
        content_id: str,
        source_language: str,
        target_language: str,
        db: AsyncSession,
    ) -> Optional[TranslationCache]:
        """
        Retrieve cached translation if available and not expired
        """
        result = await db.execute(
            select(TranslationCache).where(
                TranslationCache.content_id == content_id,
                TranslationCache.source_language == source_language,
                TranslationCache.target_language == target_language,
            )
        )
        cached = result.scalar_one_or_none()

        if cached:
            # Check if expired
            if cached.expires_at and cached.expires_at < datetime.utcnow():
                logger.debug("translation_cache_expired", content_id=content_id)
                return None

        return cached

    async def _cache_translation(
        self,
        content_id: str,
        content_type: str,
        source_language: str,
        target_language: str,
        original_text: str,
        translated_text: str,
        db: AsyncSession,
    ) -> None:
        """
        Cache translation result
        """
        try:
            # Check if cache entry exists
            existing = await self._get_cached_translation(
                content_id=content_id,
                source_language=source_language,
                target_language=target_language,
                db=db,
            )

            expires_at = datetime.utcnow() + timedelta(days=self.cache_ttl_days)

            if existing:
                # Update existing cache
                existing.original_text = original_text
                existing.translated_text = translated_text
                existing.translation_model = "gpt-4"
                existing.expires_at = expires_at
            else:
                # Create new cache entry
                cache_entry = TranslationCache(
                    source_language=source_language,
                    target_language=target_language,
                    content_type=content_type,
                    content_id=content_id,
                    original_text=original_text,
                    translated_text=translated_text,
                    translation_model="gpt-4",
                    quality_score="high",
                    expires_at=expires_at,
                )
                db.add(cache_entry)

            await db.commit()

            logger.debug(
                "translation_cached",
                content_id=content_id,
                target_language=target_language,
            )

        except Exception as e:
            logger.error("cache_error", error=str(e), content_id=content_id)
            await db.rollback()
