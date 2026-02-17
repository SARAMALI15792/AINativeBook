"""
Enhanced Content Structure Models
Implements deep-dive chapters, interactive code blocks, summaries, and variants
Sprint 1: Foundation - Database Schema Extensions
"""

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Optional
from uuid import uuid4

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum as SQLEnum,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.shared.database import Base

if TYPE_CHECKING:
    from src.core.auth.models import User
    from src.core.content.models import Content


class HierarchyType(str, Enum):
    """Content hierarchy levels"""

    STAGE = "stage"
    CHAPTER = "chapter"
    SECTION = "section"
    SUBSECTION = "subsection"


class VariantType(str, Enum):
    """Content variant types"""

    SIMPLIFIED = "simplified"  # Beginner-friendly version
    STANDARD = "standard"  # Default version
    ADVANCED = "advanced"  # Expert version with deep theory
    LANGUAGE = "language"  # Language-specific variant


class ComplexityLevel(str, Enum):
    """Content complexity levels"""

    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class SummaryType(str, Enum):
    """Summary types"""

    BRIEF = "brief"  # 2-3 sentences
    DETAILED = "detailed"  # Full paragraph
    KEY_POINTS = "key_points"  # Bullet points


class ExecutionEnvironment(str, Enum):
    """Code execution environments"""

    PYODIDE = "pyodide"  # Browser-based Python
    DOCKER = "docker"  # Server-side Docker container
    WASM = "wasm"  # WebAssembly
    LOCAL = "local"  # Local execution (for reference only)


class ContentHierarchy(Base):
    """
    Hierarchical content organization
    Enables nested structure: Stage → Chapter → Section → Subsection
    """

    __tablename__ = "content_hierarchy"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
    )
    parent_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("content_hierarchy.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    content_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("content.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Hierarchy metadata
    hierarchy_type: Mapped[HierarchyType] = mapped_column(
        SQLEnum(HierarchyType), nullable=False, index=True
    )
    order_index: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    depth_level: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )  # 0=stage, 1=chapter, 2=section, 3=subsection

    # Navigation
    slug: Mapped[str] = mapped_column(
        String(255), nullable=False, index=True
    )  # URL-friendly identifier
    breadcrumb_path: Mapped[dict] = mapped_column(
        JSONB, nullable=False, default=list
    )  # ["Stage 1", "Linux", "Kernel Theory"]

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    parent: Mapped[Optional["ContentHierarchy"]] = relationship(
        "ContentHierarchy", remote_side=[id], back_populates="children"
    )
    children: Mapped[list["ContentHierarchy"]] = relationship(
        "ContentHierarchy", back_populates="parent", cascade="all, delete-orphan"
    )
    content: Mapped["Content"] = relationship("Content", foreign_keys=[content_id])


class ContentVariant(Base):
    """
    Multiple versions of same content
    Enables personalization: simplified/standard/advanced, language variants
    """

    __tablename__ = "content_variants"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
    )
    content_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("content.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Variant metadata
    variant_type: Mapped[VariantType] = mapped_column(
        SQLEnum(VariantType), nullable=False, index=True
    )
    language_code: Mapped[str] = mapped_column(
        String(10), nullable=False, default="en", index=True
    )  # en, ur
    complexity_level: Mapped[ComplexityLevel] = mapped_column(
        SQLEnum(ComplexityLevel), nullable=False, default=ComplexityLevel.INTERMEDIATE
    )

    # Content storage
    mdx_path: Mapped[str] = mapped_column(
        String(500), nullable=False
    )  # Path to variant MDX file
    content_json: Mapped[dict] = mapped_column(
        JSONB, nullable=False
    )  # Full content snapshot with metadata

    # Quality metadata
    word_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    estimated_reading_time: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )  # minutes
    code_block_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    interactive_code_count: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )

    # Translation metadata (for language variants)
    translated_by: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True
    )  # 'human', 'gpt-4', 'google-translate'
    translation_quality_score: Mapped[Optional[float]] = mapped_column(
        Integer, nullable=True
    )  # 0.0-1.0
    reviewed_by_human: Mapped[bool] = mapped_column(Boolean, default=False)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    content: Mapped["Content"] = relationship("Content", foreign_keys=[content_id])


class ContentSummary(Base):
    """
    Chapter summaries for quick overview
    Auto-generated or manually curated
    """

    __tablename__ = "content_summaries"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
    )
    content_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("content.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Summary metadata
    summary_type: Mapped[SummaryType] = mapped_column(
        SQLEnum(SummaryType), nullable=False, index=True
    )
    language_code: Mapped[str] = mapped_column(
        String(10), nullable=False, default="en", index=True
    )

    # Summary content
    summary_text: Mapped[str] = mapped_column(Text, nullable=False)
    key_concepts: Mapped[list] = mapped_column(
        JSONB, nullable=False, default=list
    )  # ["Kernel space", "System calls", "File descriptors"]
    learning_objectives: Mapped[list] = mapped_column(
        JSONB, nullable=False, default=list
    )  # ["Understand kernel vs user space", ...]
    prerequisites: Mapped[list] = mapped_column(
        JSONB, nullable=False, default=list
    )  # ["Basic programming", "Command line"]

    # Generation metadata
    auto_generated: Mapped[bool] = mapped_column(Boolean, default=False)
    generated_by: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True
    )  # 'gpt-4', 'human'
    reviewed_by: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=False), ForeignKey("users.id"), nullable=True
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    content: Mapped["Content"] = relationship("Content", foreign_keys=[content_id])
    reviewer: Mapped[Optional["User"]] = relationship("User", foreign_keys=[reviewed_by])


class InteractiveCodeBlock(Base):
    """
    Executable code blocks within content
    Mac terminal-style editable and runnable code
    """

    __tablename__ = "interactive_code_blocks"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
    )
    content_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("content.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Code metadata
    code_language: Mapped[str] = mapped_column(
        String(50), nullable=False, index=True
    )  # python, bash, cpp, javascript
    code_content: Mapped[str] = mapped_column(Text, nullable=False)
    execution_environment: Mapped[ExecutionEnvironment] = mapped_column(
        SQLEnum(ExecutionEnvironment), nullable=False, default=ExecutionEnvironment.PYODIDE
    )

    # Execution configuration
    is_editable: Mapped[bool] = mapped_column(Boolean, default=True)
    is_executable: Mapped[bool] = mapped_column(Boolean, default=True)
    timeout_seconds: Mapped[int] = mapped_column(
        Integer, nullable=False, default=30
    )  # Max execution time
    max_output_length: Mapped[int] = mapped_column(
        Integer, nullable=False, default=10000
    )  # Max output chars

    # Expected behavior
    expected_output: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    test_cases: Mapped[list] = mapped_column(
        JSONB, nullable=False, default=list
    )  # [{"input": "...", "expected": "..."}]

    # Display configuration
    order_index: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )  # Order within content
    title: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )  # Optional title for code block
    description: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True
    )  # Explanation of what code does

    # Security & resource limits
    allowed_imports: Mapped[list] = mapped_column(
        JSONB, nullable=False, default=list
    )  # Whitelist of allowed imports
    blocked_functions: Mapped[list] = mapped_column(
        JSONB, nullable=False, default=list
    )  # Blacklist of dangerous functions
    memory_limit_mb: Mapped[int] = mapped_column(
        Integer, nullable=False, default=128
    )  # Memory limit

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    content: Mapped["Content"] = relationship("Content", foreign_keys=[content_id])


class ContentEngagement(Base):
    """
    Track user engagement with content
    Analytics for content effectiveness
    """

    __tablename__ = "content_engagement"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
    )
    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    content_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("content.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    variant_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("content_variants.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Engagement metrics
    time_spent_seconds: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    scroll_depth_percent: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )  # 0-100
    code_blocks_executed: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    exercises_completed: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    summary_viewed: Mapped[bool] = mapped_column(Boolean, default=False)

    # Personalization tracking
    language_used: Mapped[str] = mapped_column(String(10), nullable=False, default="en")
    complexity_level_used: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    # Session tracking
    session_id: Mapped[str] = mapped_column(
        String(100), nullable=False, index=True
    )  # Track individual sessions
    completed: Mapped[bool] = mapped_column(Boolean, default=False)

    # Timestamps
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), index=True
    )
    last_activity_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Relationships
    user: Mapped["User"] = relationship("User", foreign_keys=[user_id])
    content: Mapped["Content"] = relationship("Content", foreign_keys=[content_id])
    variant: Mapped[Optional["ContentVariant"]] = relationship(
        "ContentVariant", foreign_keys=[variant_id]
    )


class ContentEffectiveness(Base):
    """
    Aggregate content effectiveness metrics
    Helps identify content that needs improvement
    """

    __tablename__ = "content_effectiveness"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid4())
    )
    content_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("content.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    # Aggregate metrics
    total_views: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_completions: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    avg_completion_time_seconds: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )
    completion_rate: Mapped[float] = mapped_column(
        Integer, nullable=False, default=0.0
    )  # 0.0-1.0

    # Quality indicators
    avg_quiz_score: Mapped[Optional[float]] = mapped_column(
        Integer, nullable=True
    )  # 0.0-1.0
    user_ratings: Mapped[dict] = mapped_column(
        JSONB, nullable=False, default=dict
    )  # {"5_star": 10, "4_star": 5, ...}
    common_struggles: Mapped[list] = mapped_column(
        JSONB, nullable=False, default=list
    )  # ["Async concepts", "System calls"]

    # Engagement patterns
    avg_code_executions: Mapped[float] = mapped_column(
        Integer, nullable=False, default=0.0
    )
    summary_view_rate: Mapped[float] = mapped_column(
        Integer, nullable=False, default=0.0
    )  # % who viewed summary

    # Language preferences
    language_distribution: Mapped[dict] = mapped_column(
        JSONB, nullable=False, default=dict
    )  # {"en": 80, "ur": 20}

    # Timestamps
    last_calculated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    content: Mapped["Content"] = relationship("Content", foreign_keys=[content_id])
