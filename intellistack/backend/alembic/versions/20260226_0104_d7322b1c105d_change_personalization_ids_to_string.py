"""change_personalization_ids_to_string

Revision ID: d7322b1c105d
Revises: 20260223_user_cols
Create Date: 2026-02-26 01:04:38.732929

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
    # Drop foreign key constraints first
    op.drop_constraint('personalization_profiles_user_id_fkey', 'personalization_profiles', type_='foreignkey')
    op.drop_constraint('chapter_personalizations_profile_id_fkey', 'chapter_personalizations', type_='foreignkey')

    # Change users.id from UUID to String
    op.alter_column('users', 'id',
                    existing_type=sa.dialects.postgresql.UUID(),
                    type_=sa.String(255),
                    existing_nullable=False)

    # Change personalization_profiles columns from UUID to String
    op.alter_column('personalization_profiles', 'id',
                    existing_type=sa.dialects.postgresql.UUID(),
                    type_=sa.String(255),
                    existing_nullable=False)

    op.alter_column('personalization_profiles', 'user_id',
                    existing_type=sa.dialects.postgresql.UUID(),
                    type_=sa.String(255),
                    existing_nullable=False)

    # Change chapter_personalizations columns from UUID to String
    op.alter_column('chapter_personalizations', 'id',
                    existing_type=sa.dialects.postgresql.UUID(),
                    type_=sa.String(255),
                    existing_nullable=False)

    op.alter_column('chapter_personalizations', 'profile_id',
                    existing_type=sa.dialects.postgresql.UUID(),
                    type_=sa.String(255),
                    existing_nullable=False)

    op.alter_column('chapter_personalizations', 'content_id',
                    existing_type=sa.dialects.postgresql.UUID(),
                    type_=sa.String(255),
                    existing_nullable=False)

    # Recreate foreign key constraints
    op.create_foreign_key('personalization_profiles_user_id_fkey', 'personalization_profiles', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('chapter_personalizations_profile_id_fkey', 'chapter_personalizations', 'personalization_profiles', ['profile_id'], ['id'], ondelete='CASCADE')


def downgrade() -> None:
    # Drop foreign key constraints
    op.drop_constraint('chapter_personalizations_profile_id_fkey', 'chapter_personalizations', type_='foreignkey')
    op.drop_constraint('personalization_profiles_user_id_fkey', 'personalization_profiles', type_='foreignkey')

    # Revert chapter_personalizations columns back to UUID
    op.alter_column('chapter_personalizations', 'content_id',
                    existing_type=sa.String(255),
                    type_=sa.dialects.postgresql.UUID(),
                    existing_nullable=False)

    op.alter_column('chapter_personalizations', 'profile_id',
                    existing_type=sa.String(255),
                    type_=sa.dialects.postgresql.UUID(),
                    existing_nullable=False)

    op.alter_column('chapter_personalizations', 'id',
                    existing_type=sa.String(255),
                    type_=sa.dialects.postgresql.UUID(),
                    existing_nullable=False)

    # Revert personalization_profiles columns back to UUID
    op.alter_column('personalization_profiles', 'user_id',
                    existing_type=sa.String(255),
                    type_=sa.dialects.postgresql.UUID(),
                    existing_nullable=False)

    op.alter_column('personalization_profiles', 'id',
                    existing_type=sa.String(255),
                    type_=sa.dialects.postgresql.UUID(),
                    existing_nullable=False)

    # Revert users.id back to UUID
    op.alter_column('users', 'id',
                    existing_type=sa.String(255),
                    type_=sa.dialects.postgresql.UUID(),
                    existing_nullable=False)

    # Recreate foreign key constraints
    op.create_foreign_key('personalization_profiles_user_id_fkey', 'personalization_profiles', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('chapter_personalizations_profile_id_fkey', 'chapter_personalizations', 'personalization_profiles', ['profile_id'], ['id'], ondelete='CASCADE')
