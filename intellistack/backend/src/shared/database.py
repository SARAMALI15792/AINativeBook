"""Database configuration and session management with async SQLAlchemy."""

from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from src.config.logging import get_logger
from src.config.settings import Settings, get_settings

logger = get_logger(__name__)


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""

    pass


# Global engine and session factory (initialized on startup)
_engine = None
_async_session_factory = None


def _get_connect_args(database_url: str, statement_timeout_ms: int = 30000) -> dict:
    """
    Return connect_args based on whether the database is cloud or local.

    For asyncpg (PostgreSQL) connections we pass ``server_settings`` to set
    a per-statement timeout at the Postgres session level.  This ensures that
    a runaway query cannot block a connection indefinitely, regardless of
    application-level timeouts.

    ``statement_timeout`` is a PostgreSQL GUC that accepts milliseconds when
    passed as a string with no unit suffix via asyncpg server_settings.
    """
    if "sqlite" in database_url:
        # SQLite doesn't support pool configuration or server_settings
        return {"check_same_thread": False}
    connect_args: dict = {}
    if "neon.tech" in database_url or "sslmode=require" in database_url:
        connect_args["ssl"] = "require"
    # asyncpg exposes PostgreSQL GUCs via server_settings at connect time
    connect_args["server_settings"] = {
        "statement_timeout": str(statement_timeout_ms),
        "application_name": "intellistack-backend",
    }
    return connect_args


def init_db(settings: Settings) -> None:
    """Initialize database engine and session factory."""
    global _engine, _async_session_factory

    # Determine if using SQLite for testing
    is_sqlite = "sqlite" in settings.async_database_url

    engine_kwargs = {
        "echo": settings.debug,
        "connect_args": _get_connect_args(
            settings.database_url,
            statement_timeout_ms=settings.db_statement_timeout_ms,
        ),
    }

    # Only add pool settings for non-SQLite databases
    if not is_sqlite:
        engine_kwargs.update({
            "pool_size": settings.db_pool_size,
            "max_overflow": settings.db_max_overflow,
            "pool_timeout": settings.db_pool_timeout,
            # Recycle connections to avoid stale-connection errors on cloud DBs
            # (Neon / RDS close idle connections after a few minutes).
            "pool_recycle": settings.db_pool_recycle,
            # Verify the connection is alive before handing it to a request.
            # Adds a negligible SELECT 1 round-trip but prevents 5xx on reconnect.
            "pool_pre_ping": True,
            # Roll back any open transaction on pool return so the next borrower
            # always gets a clean connection regardless of previous usage.
            "pool_reset_on_return": "rollback",
        })

    _engine = create_async_engine(
        settings.async_database_url,
        **engine_kwargs
    )

    _async_session_factory = async_sessionmaker(
        bind=_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )


async def close_db() -> None:
    """Close database connections."""
    global _engine
    if _engine:
        await _engine.dispose()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency that provides an async database session."""
    if _async_session_factory is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")

    async with _async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


# Type alias for dependency injection
AsyncSessionDep = Annotated[AsyncSession, Depends(get_session)]


async def create_tables() -> None:
    """Create all database tables (for development/testing)."""
    if _engine is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")

    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables() -> None:
    """Drop all database tables (for testing only)."""
    if _engine is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")

    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def ensure_tables_created(settings: Settings) -> None:
    """Create tables - works for both PostgreSQL (via migrations) and SQLite (for testing)."""
    if _engine is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")

    # For SQLite (used in testing), create tables directly
    if "sqlite" in settings.async_database_url:
        logger.info("Using SQLite - creating tables directly for testing")
        try:
            async with _engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
        except Exception as e:
            # Handle "already exists" errors gracefully for SQLite
            if "already exists" in str(e).lower():
                logger.info("Tables already exist, skipping creation")
            else:
                raise
    else:
        # PostgreSQL requires migrations - skip auto-creation
        logger.info("Using PostgreSQL - tables managed via Alembic migrations")

    return


async def seed_initial_data_if_needed(settings: Settings) -> None:
    """Seed essential data (roles) if database is empty."""
    if _engine is None or _async_session_factory is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")

    from sqlalchemy import select
    from src.core.auth.models import Role, RoleName

    async with _async_session_factory() as session:
        # Check if roles exist
        result = await session.execute(select(Role).limit(1))
        if result.scalar_one_or_none():
            logger.info("Database already seeded, skipping")
            return

        # Seed essential roles
        logger.info("Seeding initial roles...")
        roles = [
            Role(name=RoleName.STUDENT.value, description="Default student user"),
            Role(name=RoleName.AUTHOR.value, description="Content author"),
            Role(name=RoleName.INSTRUCTOR.value, description="Course instructor"),
            Role(name=RoleName.INSTITUTION_ADMIN.value, description="Institution administrator"),
            Role(name=RoleName.PLATFORM_ADMIN.value, description="Platform administrator"),
        ]
        for role in roles:
            session.add(role)
        await session.commit()
        logger.info("Initial roles seeded successfully")
