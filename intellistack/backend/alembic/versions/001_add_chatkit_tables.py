"""Add ChatKit and AI tutor tables.

Revision ID: 001_add_chatkit_tables
Revises:
Create Date: 2026-02-11

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "001_add_chatkit_tables"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create ChatKit conversation and metrics tables."""
    # ChatKit Thread table
    op.create_table(
        "chatkit_thread",
        sa.Column("id", sa.String(36), nullable=False),
        sa.Column("user_id", sa.String(36), nullable=False),
        sa.Column("course_id", sa.String(36), nullable=True),
        sa.Column("title", sa.String(255), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("metadata", sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"]),
    )
    op.create_index("ix_chatkit_thread_user_id", "chatkit_thread", ["user_id"])
    op.create_index("ix_chatkit_thread_course_id", "chatkit_thread", ["course_id"])

    # ChatKit Thread Item table
    op.create_table(
        "chatkit_thread_item",
        sa.Column("id", sa.String(36), nullable=False),
        sa.Column("thread_id", sa.String(36), nullable=False),
        sa.Column("role", sa.String(20), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("metadata", sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["thread_id"], ["chatkit_thread.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_chatkit_thread_item_thread_id", "chatkit_thread_item", ["thread_id"])

    # ChatKit Rate Limit table
    op.create_table(
        "chatkit_rate_limit",
        sa.Column("id", sa.String(36), nullable=False),
        sa.Column("user_id", sa.String(36), nullable=False),
        sa.Column("message_count", sa.Integer(), nullable=False),
        sa.Column("window_start", sa.DateTime(), nullable=False),
        sa.Column("last_reset", sa.DateTime(), nullable=False),
        sa.Column("is_limited", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"]),
        sa.UniqueConstraint("user_id"),
    )
    op.create_index("ix_chatkit_rate_limit_user_id", "chatkit_rate_limit", ["user_id"])

    # AI Usage Metric table
    op.create_table(
        "ai_usage_metric",
        sa.Column("id", sa.String(36), nullable=False),
        sa.Column("user_id", sa.String(36), nullable=False),
        sa.Column("message_count", sa.Integer(), nullable=False),
        sa.Column("total_tokens", sa.Integer(), nullable=False),
        sa.Column("input_tokens", sa.Integer(), nullable=False),
        sa.Column("output_tokens", sa.Integer(), nullable=False),
        sa.Column("average_response_time_ms", sa.Integer(), nullable=False),
        sa.Column("error_count", sa.Integer(), nullable=False),
        sa.Column("date", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"]),
    )
    op.create_index("ix_ai_usage_metric_user_id", "ai_usage_metric", ["user_id"])
    op.create_index("ix_ai_usage_metric_date", "ai_usage_metric", ["date"])

    # Auth Event Log table
    op.create_table(
        "auth_event_log",
        sa.Column("id", sa.String(36), nullable=False),
        sa.Column("user_id", sa.String(36), nullable=True),
        sa.Column("event_type", sa.String(50), nullable=False),
        sa.Column("email", sa.String(255), nullable=True),
        sa.Column("ip_address", sa.String(45), nullable=True),
        sa.Column("user_agent", sa.Text(), nullable=True),
        sa.Column("reason", sa.String(255), nullable=True),
        sa.Column("metadata", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_auth_event_log_user_id", "auth_event_log", ["user_id"])
    op.create_index("ix_auth_event_log_event_type", "auth_event_log", ["event_type"])
    op.create_index("ix_auth_event_log_created_at", "auth_event_log", ["created_at"])


def downgrade() -> None:
    """Drop ChatKit and AI tutor tables."""
    op.drop_table("auth_event_log")
    op.drop_table("ai_usage_metric")
    op.drop_table("chatkit_rate_limit")
    op.drop_table("chatkit_thread_item")
    op.drop_table("chatkit_thread")
