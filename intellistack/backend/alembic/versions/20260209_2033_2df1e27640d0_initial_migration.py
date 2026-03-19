"""Initial migration

Revision ID: 2df1e27640d0
Revises:
Create Date: 2026-02-09 20:33:45.005689

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy import Text

# revision identifiers, used by Alembic.
revision: str = '2df1e27640d0'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # === Level 0: Independent tables (no foreign keys to other app tables) ===
    op.create_table('roles',
    sa.Column('id', sa.UUID(as_uuid=False), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('permissions', sa.JSON(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('stages',
    sa.Column('id', sa.UUID(as_uuid=False), nullable=False),
    sa.Column('number', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('slug', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('learning_objectives', sa.JSON(), nullable=False),
    sa.Column('prerequisite_stage_id', sa.UUID(as_uuid=False), nullable=True),
    sa.Column('estimated_hours', sa.Integer(), nullable=False),
    sa.Column('content_count', sa.Integer(), nullable=False),
    sa.Column('assessment_count', sa.Integer(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.ForeignKeyConstraint(['prerequisite_stage_id'], ['stages.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('number'),
    sa.UniqueConstraint('slug')
    )
    op.create_table('institutions',
    sa.Column('id', sa.UUID(as_uuid=False), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('slug', sa.String(length=100), nullable=False),
    sa.Column('institution_type', sa.String(length=50), nullable=False),
    sa.Column('domain', sa.String(length=255), nullable=True),
    sa.Column('logo_url', sa.String(length=500), nullable=True),
    sa.Column('primary_color', sa.String(length=7), nullable=False),
    sa.Column('secondary_color', sa.String(length=7), nullable=True),
    sa.Column('custom_css', sa.Text(), nullable=True),
    sa.Column('settings', sa.JSON(), nullable=False),
    sa.Column('welcome_message', sa.Text(), nullable=True),
    sa.Column('webhook_url', sa.String(length=500), nullable=True),
    sa.Column('webhook_secret', sa.String(length=255), nullable=True),
    sa.Column('simulation_quota_hours', sa.Integer(), nullable=False),
    sa.Column('max_students', sa.Integer(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('trial_ends_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('domain'),
    sa.UniqueConstraint('slug')
    )
    op.create_index(op.f('ix_institutions_name'), 'institutions', ['name'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.UUID(as_uuid=False), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password_hash', sa.String(length=255), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('avatar_url', sa.String(length=500), nullable=True),
    sa.Column('bio', sa.Text(), nullable=True),
    sa.Column('locale', sa.String(length=10), nullable=False),
    sa.Column('notification_settings', sa.JSON(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_deleted_at'), 'users', ['deleted_at'], unique=False)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

    # === Level 1: Tables depending on Level 0 ===
    op.create_table('badges',
    sa.Column('id', sa.UUID(as_uuid=False), nullable=False),
    sa.Column('stage_id', sa.UUID(as_uuid=False), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('icon_url', sa.String(length=500), nullable=True),
    sa.Column('criteria', sa.JSON(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.ForeignKeyConstraint(['stage_id'], ['stages.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('certificates',
    sa.Column('id', sa.UUID(as_uuid=False), nullable=False),
    sa.Column('user_id', sa.UUID(as_uuid=False), nullable=False),
    sa.Column('certificate_number', sa.String(length=50), nullable=False),
    sa.Column('issued_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('total_time_spent_hours', sa.Integer(), nullable=False),
    sa.Column('final_assessment_score', sa.Float(), nullable=True),
    sa.Column('verification_url', sa.String(length=500), nullable=True),
    sa.Column('pdf_url', sa.String(length=500), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('certificate_number')
    )
    op.create_table('cohorts',
    sa.Column('id', sa.UUID(as_uuid=False), nullable=False),
    sa.Column('institution_id', sa.UUID(as_uuid=False), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('start_date', sa.Date(), nullable=False),
    sa.Column('end_date', sa.Date(), nullable=False),
    sa.Column('enrollment_limit', sa.Integer(), nullable=True),
    sa.Column('is_enrollment_open', sa.Boolean(), nullable=False),
    sa.Column('settings', sa.JSON(), nullable=False),
    sa.Column('created_by', sa.UUID(as_uuid=False), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
    sa.ForeignKeyConstraint(['institution_id'], ['institutions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cohorts_institution_id'), 'cohorts', ['institution_id'], unique=False)
    op.create_table('content_items',
    sa.Column('id', sa.UUID(as_uuid=False), nullable=False),
    sa.Column('stage_id', sa.UUID(as_uuid=False), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('slug', sa.String(length=100), nullable=False),
    sa.Column('content_type', sa.String(length=50), nullable=False),
    sa.Column('order', sa.Integer(), nullable=False),
    sa.Column('estimated_minutes', sa.Integer(), nullable=False),
    sa.Column('content_path', sa.String(length=500), nullable=True),
    sa.Column('is_required', sa.Boolean(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.ForeignKeyConstraint(['stage_id'], ['stages.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # content table: create WITHOUT circular FK to content_versions first
    op.create_table('content',
    sa.Column('id', sa.UUID(as_uuid=False), nullable=False),
    sa.Column('stage_id', sa.UUID(as_uuid=False), nullable=False),
    sa.Column('content_type', sa.String(length=50), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('learning_objectives', sa.JSON(), nullable=False),
    sa.Column('order_index', sa.Integer(), nullable=False),
    sa.Column('mdx_path', sa.String(length=500), nullable=False),
    sa.Column('format_variants', sa.JSON(), nullable=False),
    sa.Column('current_version_id', sa.UUID(as_uuid=False), nullable=True),
    sa.Column('version_number', sa.String(length=20), nullable=False),
    sa.Column('review_status', sa.Enum('DRAFT', 'IN_REVIEW', 'PUBLISHED', 'ARCHIVED', name='contentstatus'), nullable=False),
    sa.Column('created_by', sa.UUID(as_uuid=False), nullable=False),
    sa.Column('updated_by', sa.UUID(as_uuid=False), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('published_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
    sa.ForeignKeyConstraint(['stage_id'], ['stages.id'], ),
    sa.ForeignKeyConstraint(['updated_by'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_content_review_status'), 'content', ['review_status'], unique=False)
    op.create_index(op.f('ix_content_stage_id'), 'content', ['stage_id'], unique=False)
    op.create_index(op.f('ix_content_title'), 'content', ['title'], unique=False)
    op.create_table('content_versions',
    sa.Column('id', sa.UUID(as_uuid=False), nullable=False),
    sa.Column('content_id', sa.UUID(as_uuid=False), nullable=False),
    sa.Column('version_number', sa.String(length=20), nullable=False),
    sa.Column('change_summary', sa.Text(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('content_json', sa.JSON(), nullable=False),
    sa.Column('mdx_content_hash', sa.String(length=64), nullable=False),
    sa.Column('created_by', sa.UUID(as_uuid=False), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('reviewed_by', sa.UUID(as_uuid=False), nullable=True),
    sa.Column('reviewed_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['content_id'], ['content.id'], ),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
    sa.ForeignKeyConstraint(['reviewed_by'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_content_versions_content_id'), 'content_versions', ['content_id'], unique=False)
    op.create_index(op.f('ix_content_versions_created_at'), 'content_versions', ['created_at'], unique=False)
    # Now add the circular FK from content.current_version_id -> content_versions.id
    op.create_foreign_key(
        'fk_content_current_version_id',
        'content', 'content_versions',
        ['current_version_id'], ['id']
    )
    op.create_table('content_reviews',
    sa.Column('id', sa.UUID(as_uuid=False), nullable=False),
    sa.Column('content_id', sa.UUID(as_uuid=False), nullable=False),
    sa.Column('version_id', sa.UUID(as_uuid=False), nullable=False),
    sa.Column('reviewer_id', sa.UUID(as_uuid=False), nullable=False),
    sa.Column('status', sa.Enum('PENDING', 'APPROVED', 'REJECTED', 'CHANGES_REQUESTED', name='reviewstatus'), nullable=False),
    sa.Column('comments', sa.Text(), nullable=True),
    sa.Column('rating', sa.Integer(), nullable=True),
    sa.Column('requested_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('reviewed_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['content_id'], ['content.id'], ),
    sa.ForeignKeyConstraint(['reviewer_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['version_id'], ['content_versions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_content_reviews_content_id'), 'content_reviews', ['content_id'], unique=False)
    op.create_table('institution_members',
    sa.Column('id', sa.UUID(as_uuid=False), nullable=False),
    sa.Column('institution_id', sa.UUID(as_uuid=False), nullable=False),
    sa.Column('user_id', sa.UUID(as_uuid=False), nullable=False),
    sa.Column('role', sa.String(length=50), nullable=False),
    sa.Column('joined_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('left_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['institution_id'], ['institutions.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_institution_members_institution_id'), 'institution_members', ['institution_id'], unique=False)
    op.create_index(op.f('ix_institution_members_user_id'), 'institution_members', ['user_id'], unique=False)
    op.create_table('progress',
    sa.Column('id', sa.UUID(as_uuid=False), nullable=False),
    sa.Column('user_id', sa.UUID(as_uuid=False), nullable=False),
    sa.Column('current_stage_id', sa.UUID(as_uuid=False), nullable=True),
    sa.Column('overall_percentage', sa.Float(), nullable=False),
    sa.Column('total_time_spent_minutes', sa.Integer(), nullable=False),
    sa.Column('stage_progress', sa.JSON(), nullable=False),
    sa.Column('started_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('last_activity_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['current_stage_id'], ['stages.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    op.create_table('rag_conversations',
    sa.Column('id', sa.UUID(as_uuid=False), nullable=False),
    sa.Column('user_id', sa.UUID(as_uuid=False), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_rag_conversations_user_id'), 'rag_conversations', ['user_id'], unique=False)
    op.create_table('sessions',
    sa.Column('id', sa.UUID(as_uuid=False), nullable=False),
    sa.Column('user_id', sa.UUID(as_uuid=False), nullable=False),
    sa.Column('token', sa.String(length=1000), nullable=False),
    sa.Column('user_agent', sa.String(length=500), nullable=True),
    sa.Column('ip_address', sa.String(length=45), nullable=True),
    sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('revoked_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sessions_token'), 'sessions', ['token'], unique=False)
    op.create_index(op.f('ix_sessions_user_id'), 'sessions', ['user_id'], unique=False)
    op.create_table('user_roles',
    sa.Column('id', sa.UUID(as_uuid=False), nullable=False),
    sa.Column('user_id', sa.UUID(as_uuid=False), nullable=False),
    sa.Column('role_id', sa.UUID(as_uuid=False), nullable=False),
    sa.Column('granted_by', sa.UUID(as_uuid=False), nullable=True),
    sa.Column('granted_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('revoked_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['granted_by'], ['users.id'], ),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

    # === Level 2: Tables depending on Level 1 ===
    op.create_table('cohort_enrollments',
    sa.Column('id', sa.UUID(as_uuid=False), nullable=False),
    sa.Column('cohort_id', sa.UUID(as_uuid=False), nullable=False),
    sa.Column('user_id', sa.UUID(as_uuid=False), nullable=False),
    sa.Column('enrolled_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('enrolled_by', sa.UUID(as_uuid=False), nullable=True),
    sa.Column('dropped_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['cohort_id'], ['cohorts.id'], ),
    sa.ForeignKeyConstraint(['enrolled_by'], ['users.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cohort_enrollments_cohort_id'), 'cohort_enrollments', ['cohort_id'], unique=False)
    op.create_index(op.f('ix_cohort_enrollments_user_id'), 'cohort_enrollments', ['user_id'], unique=False)
    op.create_table('cohort_instructors',
    sa.Column('id', sa.UUID(as_uuid=False), nullable=False),
    sa.Column('cohort_id', sa.UUID(as_uuid=False), nullable=False),
    sa.Column('user_id', sa.UUID(as_uuid=False), nullable=False),
    sa.Column('assigned_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('assigned_by', sa.UUID(as_uuid=False), nullable=True),
    sa.ForeignKeyConstraint(['assigned_by'], ['users.id'], ),
    sa.ForeignKeyConstraint(['cohort_id'], ['cohorts.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cohort_instructors_cohort_id'), 'cohort_instructors', ['cohort_id'], unique=False)
    op.create_index(op.f('ix_cohort_instructors_user_id'), 'cohort_instructors', ['user_id'], unique=False)
    op.create_table('content_completions',
    sa.Column('id', sa.UUID(as_uuid=False), nullable=False),
    sa.Column('progress_id', sa.UUID(as_uuid=False), nullable=False),
    sa.Column('content_item_id', sa.UUID(as_uuid=False), nullable=False),
    sa.Column('completed_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('time_spent_minutes', sa.Integer(), nullable=False),
    sa.Column('score', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['content_item_id'], ['content_items.id'], ),
    sa.ForeignKeyConstraint(['progress_id'], ['progress.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rag_messages',
    sa.Column('id', sa.UUID(as_uuid=False), nullable=False),
    sa.Column('conversation_id', sa.UUID(as_uuid=False), nullable=False),
    sa.Column('user_id', sa.UUID(as_uuid=False), nullable=False),
    sa.Column('role', sa.String(length=20), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('query', sa.Text(), nullable=True),
    sa.Column('selected_text', sa.Text(), nullable=True),
    sa.Column('confidence', sa.Float(), nullable=True),
    sa.Column('sources', sa.JSON(), nullable=False),
    sa.Column('retrieved_count', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.ForeignKeyConstraint(['conversation_id'], ['rag_conversations.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_rag_messages_conversation_id'), 'rag_messages', ['conversation_id'], unique=False)
    op.create_index(op.f('ix_rag_messages_user_id'), 'rag_messages', ['user_id'], unique=False)
    op.create_table('user_badges',
    sa.Column('id', sa.UUID(as_uuid=False), nullable=False),
    sa.Column('user_id', sa.UUID(as_uuid=False), nullable=False),
    sa.Column('badge_id', sa.UUID(as_uuid=False), nullable=False),
    sa.Column('awarded_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('awarded_for', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['badge_id'], ['badges.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

    # === Level 3: Tables depending on Level 2 ===
    op.create_table('rag_retrievals',
    sa.Column('id', sa.UUID(as_uuid=False), nullable=False),
    sa.Column('message_id', sa.UUID(as_uuid=False), nullable=False),
    sa.Column('chunk_id', sa.String(length=255), nullable=False),
    sa.Column('content_id', sa.UUID(as_uuid=False), nullable=False),
    sa.Column('stage_id', sa.UUID(as_uuid=False), nullable=False),
    sa.Column('relevance_score', sa.Float(), nullable=False),
    sa.Column('rerank_score', sa.Float(), nullable=True),
    sa.Column('was_used_in_response', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.ForeignKeyConstraint(['content_id'], ['content_items.id'], ),
    sa.ForeignKeyConstraint(['message_id'], ['rag_messages.id'], ),
    sa.ForeignKeyConstraint(['stage_id'], ['stages.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_rag_retrievals_message_id'), 'rag_retrievals', ['message_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_rag_retrievals_message_id'), table_name='rag_retrievals')
    op.drop_table('rag_retrievals')
    op.drop_table('user_badges')
    op.drop_index(op.f('ix_rag_messages_user_id'), table_name='rag_messages')
    op.drop_index(op.f('ix_rag_messages_conversation_id'), table_name='rag_messages')
    op.drop_table('rag_messages')
    op.drop_table('content_completions')
    op.drop_index(op.f('ix_cohort_instructors_user_id'), table_name='cohort_instructors')
    op.drop_index(op.f('ix_cohort_instructors_cohort_id'), table_name='cohort_instructors')
    op.drop_table('cohort_instructors')
    op.drop_index(op.f('ix_cohort_enrollments_user_id'), table_name='cohort_enrollments')
    op.drop_index(op.f('ix_cohort_enrollments_cohort_id'), table_name='cohort_enrollments')
    op.drop_table('cohort_enrollments')
    op.drop_table('user_roles')
    op.drop_index(op.f('ix_sessions_user_id'), table_name='sessions')
    op.drop_index(op.f('ix_sessions_token'), table_name='sessions')
    op.drop_table('sessions')
    op.drop_index(op.f('ix_rag_conversations_user_id'), table_name='rag_conversations')
    op.drop_table('rag_conversations')
    op.drop_table('progress')
    op.drop_index(op.f('ix_institution_members_user_id'), table_name='institution_members')
    op.drop_index(op.f('ix_institution_members_institution_id'), table_name='institution_members')
    op.drop_table('institution_members')
    op.drop_index(op.f('ix_content_reviews_content_id'), table_name='content_reviews')
    op.drop_table('content_reviews')
    # Drop circular FK before dropping content_versions
    op.drop_constraint('fk_content_current_version_id', 'content', type_='foreignkey')
    op.drop_index(op.f('ix_content_versions_created_at'), table_name='content_versions')
    op.drop_index(op.f('ix_content_versions_content_id'), table_name='content_versions')
    op.drop_table('content_versions')
    op.drop_index(op.f('ix_content_title'), table_name='content')
    op.drop_index(op.f('ix_content_stage_id'), table_name='content')
    op.drop_index(op.f('ix_content_review_status'), table_name='content')
    op.drop_table('content')
    op.drop_table('content_items')
    op.drop_index(op.f('ix_cohorts_institution_id'), table_name='cohorts')
    op.drop_table('cohorts')
    op.drop_table('certificates')
    op.drop_table('badges')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_deleted_at'), table_name='users')
    op.drop_table('users')
    op.drop_table('stages')
    op.drop_table('roles')
    op.drop_index(op.f('ix_institutions_name'), table_name='institutions')
    op.drop_table('institutions')
    # Drop enums
    sa.Enum(name='contentstatus').drop(op.get_bind(), checkfirst=True)
    sa.Enum(name='reviewstatus').drop(op.get_bind(), checkfirst=True)
    # ### end Alembic commands ###
