"""Alembic migration environment configuration."""

import asyncio
from logging.config import fileConfig
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

# Import all models to ensure they're registered with Base.metadata
from src.shared.database import Base
from src.core.auth.models import User, Role, UserRole, Session
from src.core.learning.models import (
    Stage,
    ContentItem,
    Badge,
    Progress,
    ContentCompletion,
    UserBadge,
    Certificate,
)
from src.core.institution.models import (
    Institution,
    InstitutionMember,
    Cohort,
    CohortEnrollment,
    CohortInstructor,
)
from src.core.content.models import Content, ContentVersion, ContentReview
from src.ai.rag.models import RAGConversation, RAGMessage, RAGRetrieval
from src.ai.tutor.session_store import TutorSessionItem
from src.ai.chatkit.models import ChatKitThread, ChatKitThreadItem, ChatKitRateLimit, AiUsageMetric, AuthEventLog

# Alembic Config object
config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Target metadata for 'autogenerate' support
target_metadata = Base.metadata


def get_url() -> str:
    """Get database URL from environment or config."""
    import os

    url = os.getenv("DATABASE_URL")
    if url:
        # Handle PostgreSQL URLs
        if url.startswith("postgresql://"):
            url = url.replace("postgresql://", "postgresql+asyncpg://")
            # Strip sslmode param — SSL is handled via connect_args
            if "?sslmode=" in url:
                url = url.split("?sslmode=")[0]
            elif "&sslmode=" in url:
                url = url.split("&sslmode=")[0]
        # Handle SQLite URLs
        elif url.startswith("sqlite://"):
            url = url.replace("sqlite://", "sqlite+aiosqlite://")
        return url

    # Fallback to config
    return config.get_main_option("sqlalchemy.url", "")


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL and not an Engine.
    Calls to context.execute() here emit the given string to the script output.
    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Run migrations with the given connection."""
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


def _get_connect_args() -> dict:
    """Return connect_args for SSL if using Neon or cloud PostgreSQL."""
    import os
    url = os.getenv("DATABASE_URL", "")
    if "neon.tech" in url or "sslmode=require" in url:
        return {"ssl": "require"}
    return {}


async def run_async_migrations() -> None:
    """Run migrations in 'online' mode with async engine."""

    configuration = config.get_section(config.config_ini_section) or {}
    configuration["sqlalchemy.url"] = get_url()

    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        connect_args=_get_connect_args(),
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
