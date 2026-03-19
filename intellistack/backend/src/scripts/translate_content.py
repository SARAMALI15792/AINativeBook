"""
CLI Script: Translate Content to Urdu
Batch translates all existing content to Urdu
Sprint 4: Multilingual Support
"""

import asyncio
import sys
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import structlog

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.shared.database import get_async_session
from src.core.content.models import Content
from src.core.content.enhanced_models import ContentVariant, VariantType, ComplexityLevel
from src.ai.translation.service import TranslationService
from src.ai.shared.llm_client import LLMClient

logger = structlog.get_logger()


async def translate_all_content():
    """
    Translate all existing content to Urdu
    Creates Urdu variants for all content items
    """
    print("🌍 Starting content translation to Urdu...")
    print("=" * 60)

    # Initialize services
    llm_client = LLMClient()
    translation_service = TranslationService(llm_client)

    async with get_async_session() as db:
        # Get all content
        result = await db.execute(select(Content))
        contents = result.scalars().all()

        print(f"\n📚 Found {len(contents)} content items to translate")

        translated_count = 0
        skipped_count = 0
        error_count = 0

        for i, content in enumerate(contents, 1):
            print(f"\n[{i}/{len(contents)}] Processing: {content.title}")

            try:
                # Check if Urdu variant already exists
                variant_result = await db.execute(
                    select(ContentVariant).where(
                        ContentVariant.content_id == content.id,
                        ContentVariant.language_code == "ur",
                    )
                )
                existing_variant = variant_result.scalar_one_or_none()

                if existing_variant:
                    print(f"  ⏭️  Skipped (already translated)")
                    skipped_count += 1
                    continue

                # Get English variant for content
                en_variant_result = await db.execute(
                    select(ContentVariant).where(
                        ContentVariant.content_id == content.id,
                        ContentVariant.language_code == "en",
                    )
                )
                en_variant = en_variant_result.scalar_one_or_none()

                if not en_variant:
                    print(f"  ⚠️  No English variant found, using content description")
                    content_text = content.description or content.title
                else:
                    content_text = en_variant.content_json.get("content", content.description)

                # Translate
                print(f"  🔄 Translating ({len(content_text)} chars)...")
                translated_text = await translation_service.translate_content(
                    content_id=content.id,
                    content_text=content_text,
                    source_language="en",
                    target_language="ur",
                    content_type="chapter",
                    context=content.title,
                    use_cache=True,
                    db=db,
                )

                # Create Urdu variant
                urdu_variant = ContentVariant(
                    content_id=content.id,
                    variant_type=VariantType.LANGUAGE,
                    language_code="ur",
                    complexity_level=en_variant.complexity_level if en_variant else ComplexityLevel.INTERMEDIATE,
                    mdx_path=f"{content.mdx_path.replace('.md', '.ur.md')}",
                    content_json={
                        "content": translated_text,
                        "frontmatter": {
                            "title": content.title,  # Keep English title for now
                            "language": "ur",
                        },
                    },
                    word_count=len(translated_text.split()),
                    estimated_reading_time=content.estimated_reading_time or 30,
                    translated_by="gpt-4",
                    translation_quality_score=0.9,
                    reviewed_by_human=False,
                )

                db.add(urdu_variant)
                await db.commit()

                print(f"  ✅ Translated successfully")
                translated_count += 1

            except Exception as e:
                print(f"  ❌ Error: {str(e)}")
                logger.error("translation_error", content_id=content.id, error=str(e))
                error_count += 1
                await db.rollback()
                continue

    print("\n" + "=" * 60)
    print("🎉 Translation complete!")
    print(f"  ✅ Translated: {translated_count}")
    print(f"  ⏭️  Skipped: {skipped_count}")
    print(f"  ❌ Errors: {error_count}")
    print(f"  📊 Total: {len(contents)}")


async def translate_specific_content(content_id: str):
    """
    Translate a specific content item to Urdu
    """
    print(f"🌍 Translating content: {content_id}")

    llm_client = LLMClient()
    translation_service = TranslationService(llm_client)

    async with get_async_session() as db:
        # Get content
        result = await db.execute(
            select(Content).where(Content.id == content_id)
        )
        content = result.scalar_one_or_none()

        if not content:
            print(f"❌ Content not found: {content_id}")
            return

        print(f"📄 Title: {content.title}")

        # Get English variant
        variant_result = await db.execute(
            select(ContentVariant).where(
                ContentVariant.content_id == content.id,
                ContentVariant.language_code == "en",
            )
        )
        en_variant = variant_result.scalar_one_or_none()

        content_text = en_variant.content_json.get("content", content.description) if en_variant else content.description

        # Translate
        print(f"🔄 Translating...")
        translated_text = await translation_service.translate_content(
            content_id=content.id,
            content_text=content_text,
            source_language="en",
            target_language="ur",
            content_type="chapter",
            context=content.title,
            use_cache=True,
            db=db,
        )

        # Create Urdu variant
        urdu_variant = ContentVariant(
            content_id=content.id,
            variant_type=VariantType.LANGUAGE,
            language_code="ur",
            complexity_level=en_variant.complexity_level if en_variant else ComplexityLevel.INTERMEDIATE,
            mdx_path=f"{content.mdx_path.replace('.md', '.ur.md')}",
            content_json={
                "content": translated_text,
                "frontmatter": {
                    "title": content.title,
                    "language": "ur",
                },
            },
            word_count=len(translated_text.split()),
            estimated_reading_time=content.estimated_reading_time or 30,
            translated_by="gpt-4",
            translation_quality_score=0.9,
            reviewed_by_human=False,
        )

        db.add(urdu_variant)
        await db.commit()

        print(f"✅ Translation complete!")
        print(f"📊 Word count: {urdu_variant.word_count}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Translate content to Urdu")
    parser.add_argument(
        "--content-id",
        type=str,
        help="Translate specific content by ID",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Translate all content",
    )

    args = parser.parse_args()

    if args.content_id:
        asyncio.run(translate_specific_content(args.content_id))
    elif args.all:
        asyncio.run(translate_all_content())
    else:
        print("Usage:")
        print("  python translate_content.py --all")
        print("  python translate_content.py --content-id <content_id>")
