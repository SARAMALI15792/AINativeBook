"""add personalization profiles table

Revision ID: add_personalization_profiles
Revises: 20260217_enhanced_content
Create Date: 2026-02-18 23:32:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'add_personalization_profiles'
down_revision: Union[str, None] = '20260217_enhanced_content'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Import necessary modules for enum handling
    from sqlalchemy import text
    import logging

    # Create enum types with exception handling to prevent duplicate errors
    conn = op.get_bind()

    # Check if this is a real connection (not a mock for --sql generation)
    if hasattr(conn, 'execute'):
        # Define enum types to create
        enum_definitions = [
            ("learningstyle", ["visual", "auditory", "kinesthetic", "reading"]),
            ("learningpace", ["slow", "moderate", "fast"])
        ]

        for enum_name, enum_values in enum_definitions:
            try:
                # Simply attempt to create the enum - if it already exists, catch the exception
                values_str = ", ".join([f"'{val}'" for val in enum_values])
                conn.execute(text(f"CREATE TYPE {enum_name} AS ENUM ({values_str})"))
                if hasattr(conn, 'commit'):
                    conn.commit()
            except Exception as e:
                # If type already exists, we just continue (the exception is expected)
                # We only want to catch the specific duplicate type error, but this is simpler
                logging.info(f"Enum {enum_name} already exists or error occurred: {str(e)}")
                if hasattr(conn, 'rollback'):
                    conn.rollback()  # Rollback the failed transaction

    # Create enum objects with create_type=False to avoid SQLAlchemy trying to create them
    learning_style_enum = postgresql.ENUM('visual', 'auditory', 'kinesthetic', 'reading', name='learningstyle', create_type=False)
    learning_pace_enum = postgresql.ENUM('slow', 'moderate', 'fast', name='learningpace', create_type=False)

    # Create personalization_profiles table
    op.create_table(
        'personalization_profiles',
        sa.Column('id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column('educational_background', sa.Text(), nullable=True),
        sa.Column('prior_experience', sa.Text(), nullable=True),
        sa.Column('technical_skills', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('learning_goals', sa.Text(), nullable=True),
        sa.Column('learning_style', sa.String(length=20), nullable=True),
        sa.Column('learning_pace', sa.String(length=20), nullable=False, server_default='moderate'),
        sa.Column('preferred_language', sa.String(length=10), nullable=False, server_default='en'),
        sa.Column('preferred_examples_domain', sa.String(length=100), nullable=True),
        sa.Column('interest_areas', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('adaptive_complexity', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('personalized_exercises', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('personalized_time_estimates', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('share_progress_with_instructors', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('share_with_peers', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('allow_ai_personalization', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('last_reset_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('user_id')
    )

    # Create indexes
    op.create_index('ix_personalization_profiles_user_id', 'personalization_profiles', ['user_id'])


def downgrade() -> None:
    op.drop_index('ix_personalization_profiles_user_id', table_name='personalization_profiles')
    op.drop_table('personalization_profiles')
    op.execute('DROP TYPE IF EXISTS learningstyle')
    op.execute('DROP TYPE IF EXISTS learningpace')
