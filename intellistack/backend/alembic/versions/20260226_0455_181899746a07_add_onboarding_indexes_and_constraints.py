"""add_onboarding_indexes_and_constraints

Revision ID: 181899746a07
Revises: d7322b1c105d
Create Date: 2026-02-26 04:55:41.158261

Add indexes and check constraints for onboarding columns to improve
query performance and enforce data integrity.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '181899746a07'
down_revision: Union[str, None] = 'd7322b1c105d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add indexes for onboarding_completed and current_stage (T002)
    op.execute("""
        CREATE INDEX IF NOT EXISTS idx_users_onboarding_completed
        ON users(onboarding_completed);
    """)

    op.execute("""
        CREATE INDEX IF NOT EXISTS idx_users_current_stage
        ON users(current_stage);
    """)

    # Add check constraints (T003)
    # Constraint for current_stage (must be between 1 and 5)
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM pg_constraint
                WHERE conname = 'chk_users_current_stage'
            ) THEN
                ALTER TABLE users
                ADD CONSTRAINT chk_users_current_stage
                CHECK (current_stage >= 1 AND current_stage <= 5);
            END IF;
        END $$;
    """)

    # Constraint for role (must be student, instructor, or admin)
    op.execute("""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM pg_constraint
                WHERE conname = 'chk_users_role'
            ) THEN
                ALTER TABLE users
                ADD CONSTRAINT chk_users_role
                CHECK (role IN ('student', 'instructor', 'admin'));
            END IF;
        END $$;
    """)


def downgrade() -> None:
    # Remove check constraints
    op.execute("ALTER TABLE users DROP CONSTRAINT IF EXISTS chk_users_role;")
    op.execute("ALTER TABLE users DROP CONSTRAINT IF EXISTS chk_users_current_stage;")

    # Remove indexes
    op.execute("DROP INDEX IF EXISTS idx_users_current_stage;")
    op.execute("DROP INDEX IF EXISTS idx_users_onboarding_completed;")
