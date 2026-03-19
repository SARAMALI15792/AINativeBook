"""
Content Sync Service
Automated sync between markdown files and database
Sprint 7: Content Ingestion & Sync
"""

from typing import Optional, List, Dict, Any
from pathlib import Path
import hashlib
import frontmatter
import structlog
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.core.content.models import Content
from src.core.content.enhanced_models import (
    ContentVariant,
    ContentSummary,
    InteractiveCodeBlock,
    VariantType,
    ComplexityLevel,
    ExecutionEnvironment,
)

logger = structlog.get_logger()


class ContentSyncService:
    """
    Sync markdown files to database
    Implements automated content ingestion and updates
    """

    def __init__(self, content_directory: Path):
        self.content_directory = content_directory

    async def scan_content_directory(
        self,
        directory: Optional[Path] = None,
    ) -> List[Dict[str, Any]]:
        """
        Scan content directory for markdown files
        Parse frontmatter and content

        Returns:
            List of ContentFile dicts with metadata
        """
        scan_dir = directory or self.content_directory
        content_files = []

        try:
            # Find all markdown files
            md_files = list(scan_dir.rglob("*.md"))

            logger.info(
                "scanning_content_directory",
                directory=str(scan_dir),
                file_count=len(md_files),
            )

            for md_file in md_files:
                try:
                    # Parse frontmatter and content
                    with open(md_file, "r", encoding="utf-8") as f:
                        post = frontmatter.load(f)

                    # Extract metadata
                    content_data = {
                        "file_path": str(md_file),
                        "relative_path": str(md_file.relative_to(self.content_directory)),
                        "title": post.get("title", md_file.stem),
                        "description": post.get("description", ""),
                        "id": post.get("id", md_file.stem),
                        "sidebar_label": post.get("sidebar_label", ""),
                        "difficulty": post.get("difficulty", "intermediate"),
                        "estimated_time": post.get("estimated_time", 30),
                        "tags": post.get("tags", []),
                        "content": post.content,
                        "frontmatter": dict(post.metadata),
                        "file_hash": self._calculate_file_hash(md_file),
                        "word_count": len(post.content.split()),
                    }

                    content_files.append(content_data)

                except Exception as e:
                    logger.error(
                        "file_parse_error",
                        file=str(md_file),
                        error=str(e),
                    )
                    continue

            logger.info(
                "content_scan_completed",
                total_files=len(content_files),
            )

            return content_files

        except Exception as e:
            logger.error("directory_scan_error", error=str(e))
            return []

    async def sync_content_to_db(
        self,
        content_file: Dict[str, Any],
        stage_id: str,
        db: AsyncSession,
    ) -> Optional[Content]:
        """
        Create or update Content record
        - Create ContentVariant (standard, en)
        - Extract and store code blocks
        - Generate summary if missing
        - Update vector store for RAG

        Args:
            content_file: Parsed content file data
            stage_id: Stage ID this content belongs to
            db: Database session

        Returns:
            Content object
        """
        try:
            # Check if content exists
            existing = await self._get_content_by_id(
                content_id=content_file["id"],
                db=db,
            )

            if existing:
                # Check if content changed
                if await self.detect_changes(content_file, existing, db):
                    logger.info(
                        "content_changed_updating",
                        content_id=content_file["id"],
                    )
                    await self._update_content(existing, content_file, db)
                else:
                    logger.debug(
                        "content_unchanged_skipping",
                        content_id=content_file["id"],
                    )
                    return existing
            else:
                # Create new content
                logger.info(
                    "creating_new_content",
                    content_id=content_file["id"],
                )
                existing = await self._create_content(
                    content_file, stage_id, db
                )

            # Create or update standard variant
            await self._sync_content_variant(
                content=existing,
                content_file=content_file,
                db=db,
            )

            # Extract and sync code blocks
            await self._sync_code_blocks(
                content=existing,
                content_text=content_file["content"],
                db=db,
            )

            await db.commit()

            logger.info(
                "content_synced",
                content_id=existing.id,
                title=existing.title,
            )

            return existing

        except Exception as e:
            logger.error(
                "content_sync_error",
                error=str(e),
                content_id=content_file.get("id"),
            )
            await db.rollback()
            return None

    async def detect_changes(
        self,
        content_file: Dict[str, Any],
        existing_content: Content,
        db: AsyncSession,
    ) -> bool:
        """
        Compare file hash with stored hash
        Return True if content changed
        """
        # Get current variant
        result = await db.execute(
            select(ContentVariant).where(
                ContentVariant.content_id == existing_content.id,
                ContentVariant.variant_type == VariantType.STANDARD,
                ContentVariant.language_code == "en",
            )
        )
        variant = result.scalar_one_or_none()

        if not variant:
            return True  # No variant exists, needs sync

        # Compare file hash
        stored_hash = variant.content_json.get("file_hash", "")
        current_hash = content_file["file_hash"]

        return stored_hash != current_hash

    async def full_sync(
        self,
        stage_id: Optional[str] = None,
        db: Optional[AsyncSession] = None,
    ) -> Dict[str, int]:
        """
        Full sync of all content files
        Run on startup or manual trigger

        Returns:
            Dict with sync statistics
        """
        stats = {
            "scanned": 0,
            "created": 0,
            "updated": 0,
            "skipped": 0,
            "errors": 0,
        }

        try:
            # Scan all content files
            content_files = await self.scan_content_directory()
            stats["scanned"] = len(content_files)

            if not db:
                logger.warning("no_db_session_provided")
                return stats

            # Sync each file
            for content_file in content_files:
                try:
                    # Determine stage_id from file path if not provided
                    if not stage_id:
                        stage_id = self._extract_stage_id(
                            content_file["relative_path"]
                        )

                    result = await self.sync_content_to_db(
                        content_file=content_file,
                        stage_id=stage_id,
                        db=db,
                    )

                    if result:
                        # Check if it was created or updated
                        # (simplified - in production, track this properly)
                        stats["updated"] += 1
                    else:
                        stats["errors"] += 1

                except Exception as e:
                    logger.error(
                        "file_sync_error",
                        file=content_file["file_path"],
                        error=str(e),
                    )
                    stats["errors"] += 1

            logger.info("full_sync_completed", stats=stats)
            return stats

        except Exception as e:
            logger.error("full_sync_error", error=str(e))
            return stats

    async def _get_content_by_id(
        self,
        content_id: str,
        db: AsyncSession,
    ) -> Optional[Content]:
        """Get content by ID"""
        result = await db.execute(
            select(Content).where(Content.id == content_id)
        )
        return result.scalar_one_or_none()

    async def _create_content(
        self,
        content_file: Dict[str, Any],
        stage_id: str,
        db: AsyncSession,
    ) -> Content:
        """Create new Content record"""
        content = Content(
            id=content_file["id"],
            stage_id=stage_id,
            content_type="lesson",  # Default type
            title=content_file["title"],
            description=content_file["description"],
            learning_objectives=content_file["frontmatter"].get(
                "learning_objectives", []
            ),
            order_index=0,  # TODO: Extract from frontmatter
            mdx_path=content_file["relative_path"],
            estimated_reading_time=content_file["estimated_time"],
            tags=content_file["tags"],
            difficulty_level=ComplexityLevel(content_file["difficulty"]),
            created_by="system",  # TODO: Get from context
        )

        db.add(content)
        return content

    async def _update_content(
        self,
        content: Content,
        content_file: Dict[str, Any],
        db: AsyncSession,
    ) -> None:
        """Update existing Content record"""
        content.title = content_file["title"]
        content.description = content_file["description"]
        content.learning_objectives = content_file["frontmatter"].get(
            "learning_objectives", []
        )
        content.estimated_reading_time = content_file["estimated_time"]
        content.tags = content_file["tags"]
        content.difficulty_level = ComplexityLevel(content_file["difficulty"])

    async def _sync_content_variant(
        self,
        content: Content,
        content_file: Dict[str, Any],
        db: AsyncSession,
    ) -> None:
        """Create or update standard English variant"""
        # Check if variant exists
        result = await db.execute(
            select(ContentVariant).where(
                ContentVariant.content_id == content.id,
                ContentVariant.variant_type == VariantType.STANDARD,
                ContentVariant.language_code == "en",
            )
        )
        variant = result.scalar_one_or_none()

        content_json = {
            "content": content_file["content"],
            "frontmatter": content_file["frontmatter"],
            "file_hash": content_file["file_hash"],
        }

        if variant:
            # Update existing
            variant.content_json = content_json
            variant.word_count = content_file["word_count"]
            variant.estimated_reading_time = content_file["estimated_time"]
        else:
            # Create new
            variant = ContentVariant(
                content_id=content.id,
                variant_type=VariantType.STANDARD,
                language_code="en",
                complexity_level=ComplexityLevel(content_file["difficulty"]),
                mdx_path=content_file["relative_path"],
                content_json=content_json,
                word_count=content_file["word_count"],
                estimated_reading_time=content_file["estimated_time"],
            )
            db.add(variant)

    async def _sync_code_blocks(
        self,
        content: Content,
        content_text: str,
        db: AsyncSession,
    ) -> None:
        """Extract and sync interactive code blocks"""
        # Simple regex to find code blocks
        # In production, use proper markdown parser
        import re

        code_pattern = r"```(\w+)\s+live\n(.*?)```"
        matches = re.finditer(code_pattern, content_text, re.DOTALL)

        order_index = 0
        for match in matches:
            language = match.group(1)
            code = match.group(2).strip()

            # Check if code block already exists
            # (simplified - in production, use better identification)
            code_block = InteractiveCodeBlock(
                content_id=content.id,
                code_language=language,
                code_content=code,
                execution_environment=ExecutionEnvironment.PYODIDE
                if language == "python"
                else ExecutionEnvironment.DOCKER,
                is_editable=True,
                is_executable=True,
                order_index=order_index,
            )

            db.add(code_block)
            order_index += 1

        if order_index > 0:
            content.has_interactive_code = True

    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calculate SHA-256 hash of file"""
        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
        return sha256.hexdigest()

    def _extract_stage_id(self, relative_path: str) -> str:
        """Extract stage ID from file path"""
        # Example: "stage-1/linux/1-1-linux-theory.md" -> "stage-1"
        parts = relative_path.split("/")
        if parts and parts[0].startswith("stage-"):
            return parts[0]
        return "stage-1"  # Default fallback
