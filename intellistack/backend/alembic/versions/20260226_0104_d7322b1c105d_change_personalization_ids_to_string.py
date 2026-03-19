"""change_personalization_ids_to_string

Revision ID: d7322b1c105d
Revises: 20260223_user_cols
Create Date: 2026-02-26 01:04:38.732929

NOTE: This migration has been disabled due to schema inconsistencies.
The type conversion from UUID to String causes cascading constraint issues.
The application will use UUID for users.id and handle String conversions at the application level.

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd7322b1c105d'
down_revision: Union[str, None] = '20260223_user_cols'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # This migration is disabled - no operations performed
    # Type conversion creates circular dependency issues with foreign keys
    pass


def downgrade() -> None:
    # This migration is disabled - no operations performed
    pass
