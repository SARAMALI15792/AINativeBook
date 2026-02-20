"""Enhanced content structure with deep-dive chapters

Revision ID: 20260217_enhanced_content
Revises: 001_add_chatkit_tables
Create Date: 2026-02-17 17:25:00.000000

Sprint 1: Foundation - Database Schema Extensions
Adds: ContentHierarchy, ContentVariant, ContentSummary, InteractiveCodeBlock,
      ContentEngagement, ContentEffectiveness
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '20260217_enhanced_content'
down_revision: Union[str, None] = '001_add_chatkit_tables'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Import necessary modules for enum handling
    from sqlalchemy import text
    import logging

    # Create enum types with exception handling to prevent duplicate errors
    conn = op.get_bind()

    # Define enum types to create
    enum_definitions = [
        ("hierarchytype", ["stage", "chapter", "section", "subsection"]),
        ("varianttype", ["simplified", "standard", "advanced", "language"]),
        ("complexitylevel", ["beginner", "intermediate", "advanced"]),
        ("summarytype", ["brief", "detailed", "key_points"]),
        ("executionenvironment", ["pyodide", "docker", "wasm", "local"])
    ]

    for enum_name, enum_values in enum_definitions:
        try:
            # Simply attempt to create the enum - if it already exists, catch the exception
            values_str = ", ".join([f"'{val}'" for val in enum_values])
            conn.execute(text(f"CREATE TYPE {enum_name} AS ENUM ({values_str})"))
            conn.commit()
        except Exception as e:
            # If type already exists, we just continue (the exception is expected)
            # We only want to catch the specific duplicate type error, but this is simpler
            logging.info(f"Enum {enum_name} already exists or error occurred: {str(e)}")
            conn.rollback()  # Rollback the failed transaction

    # ContentHierarchy table
    op.create_table(
        'content_hierarchy',
        sa.Column('id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column('parent_id', postgresql.UUID(as_uuid=False), nullable=True),
        sa.Column('content_id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column('hierarchy_type', sa.Enum('stage', 'chapter', 'section', 'subsection', name='hierarchytype', create_type=False), nullable=False),
        sa.Column('order_index', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('depth_level', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('slug', sa.String(length=255), nullable=False),
        sa.Column('breadcrumb_path', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default='[]'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['parent_id'], ['content_hierarchy.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['content_id'], ['content.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_content_hierarchy_parent_id', 'content_hierarchy', ['parent_id'])
    op.create_index('ix_content_hierarchy_content_id', 'content_hierarchy', ['content_id'])
    op.create_index('ix_content_hierarchy_hierarchy_type', 'content_hierarchy', ['hierarchy_type'])
    op.create_index('ix_content_hierarchy_slug', 'content_hierarchy', ['slug'])

    # ContentVariant table
    op.create_table(
        'content_variants',
        sa.Column('id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column('content_id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column('variant_type', sa.Enum('simplified', 'standard', 'advanced', 'language', name='varianttype', create_type=False), nullable=False),
        sa.Column('language_code', sa.String(length=10), nullable=False, server_default='en'),
        sa.Column('complexity_level', sa.Enum('beginner', 'intermediate', 'advanced', name='complexitylevel', create_type=False), nullable=False, server_default='intermediate'),
        sa.Column('mdx_path', sa.String(length=500), nullable=False),
        sa.Column('content_json', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('word_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('estimated_reading_time', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('code_block_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('interactive_code_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('translated_by', sa.String(length=50), nullable=True),
        sa.Column('translation_quality_score', sa.Float(), nullable=True),
        sa.Column('reviewed_by_human', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['content_id'], ['content.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_content_variants_content_id', 'content_variants', ['content_id'])
    op.create_index('ix_content_variants_variant_type', 'content_variants', ['variant_type'])
    op.create_index('ix_content_variants_language_code', 'content_variants', ['language_code'])

    # ContentSummary table
    op.create_table(
        'content_summaries',
        sa.Column('id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column('content_id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column('summary_type', sa.Enum('brief', 'detailed', 'key_points', name='summarytype', create_type=False), nullable=False),
        sa.Column('language_code', sa.String(length=10), nullable=False, server_default='en'),
        sa.Column('summary_text', sa.Text(), nullable=False),
        sa.Column('key_concepts', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default='[]'),
        sa.Column('learning_objectives', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default='[]'),
        sa.Column('prerequisites', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default='[]'),
        sa.Column('auto_generated', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('generated_by', sa.String(length=50), nullable=True),
        sa.Column('reviewed_by', postgresql.UUID(as_uuid=False), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['content_id'], ['content.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['reviewed_by'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_content_summaries_content_id', 'content_summaries', ['content_id'])
    op.create_index('ix_content_summaries_summary_type', 'content_summaries', ['summary_type'])
    op.create_index('ix_content_summaries_language_code', 'content_summaries', ['language_code'])

    # InteractiveCodeBlock table
    op.create_table(
        'interactive_code_blocks',
        sa.Column('id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column('content_id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column('code_language', sa.String(length=50), nullable=False),
        sa.Column('code_content', sa.Text(), nullable=False),
        sa.Column('execution_environment', sa.Enum('pyodide', 'docker', 'wasm', 'local', name='executionenvironment', create_type=False), nullable=False, server_default='pyodide'),
        sa.Column('is_editable', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('is_executable', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('timeout_seconds', sa.Integer(), nullable=False, server_default='30'),
        sa.Column('max_output_length', sa.Integer(), nullable=False, server_default='10000'),
        sa.Column('expected_output', sa.Text(), nullable=True),
        sa.Column('test_cases', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default='[]'),
        sa.Column('order_index', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('title', sa.String(length=255), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('allowed_imports', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default='[]'),
        sa.Column('blocked_functions', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default='[]'),
        sa.Column('memory_limit_mb', sa.Integer(), nullable=False, server_default='128'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['content_id'], ['content.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_interactive_code_blocks_content_id', 'interactive_code_blocks', ['content_id'])
    op.create_index('ix_interactive_code_blocks_code_language', 'interactive_code_blocks', ['code_language'])

    # ContentEngagement table
    op.create_table(
        'content_engagement',
        sa.Column('id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column('content_id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column('variant_id', postgresql.UUID(as_uuid=False), nullable=True),
        sa.Column('time_spent_seconds', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('scroll_depth_percent', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('code_blocks_executed', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('exercises_completed', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('summary_viewed', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('language_used', sa.String(length=10), nullable=False, server_default='en'),
        sa.Column('complexity_level_used', sa.String(length=20), nullable=True),
        sa.Column('session_id', sa.String(length=100), nullable=False),
        sa.Column('completed', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('started_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('last_activity_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['content_id'], ['content.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['variant_id'], ['content_variants.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_content_engagement_user_id', 'content_engagement', ['user_id'])
    op.create_index('ix_content_engagement_content_id', 'content_engagement', ['content_id'])
    op.create_index('ix_content_engagement_session_id', 'content_engagement', ['session_id'])
    op.create_index('ix_content_engagement_started_at', 'content_engagement', ['started_at'])

    # ContentEffectiveness table
    op.create_table(
        'content_effectiveness',
        sa.Column('id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column('content_id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column('total_views', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('total_completions', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('avg_completion_time_seconds', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('completion_rate', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('avg_quiz_score', sa.Float(), nullable=True),
        sa.Column('user_ratings', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default='{}'),
        sa.Column('common_struggles', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default='[]'),
        sa.Column('avg_code_executions', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('summary_view_rate', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('language_distribution', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default='{}'),
        sa.Column('last_calculated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['content_id'], ['content.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('content_id')
    )
    op.create_index('ix_content_effectiveness_content_id', 'content_effectiveness', ['content_id'], unique=True)

    # Add new fields to existing Content table
    op.add_column('content', sa.Column('has_summary', sa.Boolean(), nullable=False, server_default='false'))
    op.add_column('content', sa.Column('has_interactive_code', sa.Boolean(), nullable=False, server_default='false'))
    op.add_column('content', sa.Column('difficulty_level', sa.Enum('beginner', 'intermediate', 'advanced', name='complexitylevel', create_type=False), nullable=False, server_default='intermediate'))
    op.add_column('content', sa.Column('estimated_reading_time', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('content', sa.Column('prerequisites', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default='[]'))
    op.add_column('content', sa.Column('related_content', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default='[]'))
    op.add_column('content', sa.Column('tags', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default='[]'))
    op.add_column('content', sa.Column('keywords', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default='[]'))


def downgrade() -> None:
    # Remove new columns from Content table
    op.drop_column('content', 'keywords')
    op.drop_column('content', 'tags')
    op.drop_column('content', 'related_content')
    op.drop_column('content', 'prerequisites')
    op.drop_column('content', 'estimated_reading_time')
    op.drop_column('content', 'difficulty_level')
    op.drop_column('content', 'has_interactive_code')
    op.drop_column('content', 'has_summary')

    # Drop tables
    op.drop_index('ix_content_effectiveness_content_id', table_name='content_effectiveness')
    op.drop_table('content_effectiveness')

    op.drop_index('ix_content_engagement_started_at', table_name='content_engagement')
    op.drop_index('ix_content_engagement_session_id', table_name='content_engagement')
    op.drop_index('ix_content_engagement_content_id', table_name='content_engagement')
    op.drop_index('ix_content_engagement_user_id', table_name='content_engagement')
    op.drop_table('content_engagement')

    op.drop_index('ix_interactive_code_blocks_code_language', table_name='interactive_code_blocks')
    op.drop_index('ix_interactive_code_blocks_content_id', table_name='interactive_code_blocks')
    op.drop_table('interactive_code_blocks')

    op.drop_index('ix_content_summaries_language_code', table_name='content_summaries')
    op.drop_index('ix_content_summaries_summary_type', table_name='content_summaries')
    op.drop_index('ix_content_summaries_content_id', table_name='content_summaries')
    op.drop_table('content_summaries')

    op.drop_index('ix_content_variants_language_code', table_name='content_variants')
    op.drop_index('ix_content_variants_variant_type', table_name='content_variants')
    op.drop_index('ix_content_variants_content_id', table_name='content_variants')
    op.drop_table('content_variants')

    op.drop_index('ix_content_hierarchy_slug', table_name='content_hierarchy')
    op.drop_index('ix_content_hierarchy_hierarchy_type', table_name='content_hierarchy')
    op.drop_index('ix_content_hierarchy_content_id', table_name='content_hierarchy')
    op.drop_index('ix_content_hierarchy_parent_id', table_name='content_hierarchy')
    op.drop_table('content_hierarchy')

    # Drop enum types only if they exist
    op.execute("DROP TYPE IF EXISTS executionenvironment")
    op.execute("DROP TYPE IF EXISTS summarytype")
    op.execute("DROP TYPE IF EXISTS complexitylevel")
    op.execute("DROP TYPE IF EXISTS varianttype")
    op.execute("DROP TYPE IF EXISTS hierarchytype")
