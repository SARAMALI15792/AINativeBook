"""Add missing columns to chatkit_thread table.

lesson_stage, status, and enrollment_ended_at were defined in the SQLAlchemy
model and used in store.py but were never added to the migration.

Revision ID: 20260321_chatkit_cols
Revises: 181899746a07
Create Date: 2026-03-21
"""
from alembic import op
import sqlalchemy as sa


revision = "20260321_chatkit_cols"
down_revision = "181899746a07"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "chatkit_thread",
        sa.Column("lesson_stage", sa.Integer(), nullable=True),
    )
    op.add_column(
        "chatkit_thread",
        sa.Column("status", sa.String(20), nullable=False, server_default="active"),
    )
    op.add_column(
        "chatkit_thread",
        sa.Column("enrollment_ended_at", sa.DateTime(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("chatkit_thread", "enrollment_ended_at")
    op.drop_column("chatkit_thread", "status")
    op.drop_column("chatkit_thread", "lesson_stage")
