"""Database type utilities for cross-database compatibility."""
from typing import Union
from sqlalchemy import JSON
from sqlalchemy.dialects.postgresql import UUID as _UUID


def UUID(as_uuid: bool = False):
    """Return appropriate UUID type based on database dialect."""
    return _UUID(as_uuid=as_uuid)  # Will be used for PostgreSQL


def get_json_type():
    """Get the appropriate JSON type for the current database dialect."""
    return JSON


def is_postgresql_url(database_url: str) -> bool:
    """Check if the database URL is for PostgreSQL."""
    return "postgresql" in database_url


def is_sqlite_url(database_url: str) -> bool:
    """Check if the database URL is for SQLite."""
    return "sqlite" in database_url