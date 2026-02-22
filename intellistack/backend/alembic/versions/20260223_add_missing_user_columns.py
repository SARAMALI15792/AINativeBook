"""Add missing user columns (email_verified, onboarding_completed, current_stage, role, preferences)

Revision ID: 20260223_add_missing_user_columns
Revises: add_personalization_profiles
Create Date: 2026-02-23 03:14:00.000000

These columns exist in the User SQLAlchemy model but were never added
to the database via migration, causing 500 errors on all authenticated
endpoints (sync_user_from_jwt fails on INSERT/SELECT with missing columns).
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '20260223_add_missing_user_columns'
down_revision: Union[str, None] = 'add_personalization_profiles'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add email_verified column (Boolean, default False)
    op.add_column('users', sa.Column(
        'email_verified',
        sa.Boolean(),
        nullable=False,
        server_default='false',
    ))

    # Add onboarding_completed column (Boolean, default False)
    op.add_column('users', sa.Column(
        'onboarding_completed',
        sa.Boolean(),
        nullable=False,
        server_default='false',
    ))

    # Add current_stage column (Integer, default 1)
    op.add_column('users', sa.Column(
        'current_stage',
        sa.Integer(),
        nullable=False,
        server_default='1',
    ))

    # Add role column (String(50), default 'student', nullable)
    op.add_column('users', sa.Column(
        'role',
        sa.String(length=50),
        nullable=True,
        server_default='student',
    ))

    # Add preferences column (JSONB, nullable)
    op.add_column('users', sa.Column(
        'preferences',
        postgresql.JSONB(astext_type=sa.Text()),
        nullable=True,
    ))


def downgrade() -> None:
    op.drop_column('users', 'preferences')
    op.drop_column('users', 'role')
    op.drop_column('users', 'current_stage')
    op.drop_column('users', 'onboarding_completed')
    op.drop_column('users', 'email_verified')
