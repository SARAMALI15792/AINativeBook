import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from src.shared.database import AsyncSessionDep


@pytest.mark.asyncio
async def test_database_session_fixture(db_session: AsyncSession):
    """Test that the database session fixture works correctly."""
    assert db_session is not None
    assert isinstance(db_session, AsyncSession)

    # Test that the session can be used
    result = await db_session.execute(text("SELECT 1"))
    assert result is not None