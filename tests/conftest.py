import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock
import os
from unittest.mock import patch

from intellistack.backend.src.config.settings import get_settings
from intellistack.backend.src.shared.database import Base


# Create an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def setup_test_settings():
    """Set up test environment variables."""
    # Store original environment
    original_env = os.environ.copy()

    # Set test environment variables
    test_vars = {
        "SECRET_KEY": "test-secret-key-for-testing-with-32-chars-at-least",
        "DATABASE_URL": "sqlite+aiosqlite:///:memory:",
        "REDIS_URL": "redis://localhost:6379",
        "QDRANT_HOST": "localhost",
        "GOOGLE_REDIRECT_URI": "http://localhost:3000/api/auth/callback/google",
        "GITHUB_REDIRECT_URI": "http://localhost:3000/api/auth/callback/github",
        "BETTER_AUTH_URL": "http://localhost:3000",
        "BETTER_AUTH_JWKS_URL": "http://localhost:3000/.well-known/jwks.json",
        "ENVIRONMENT": "development",  # Changed from 'test' to 'development'
        "DEBUG": "True",
        "LOG_LEVEL": "DEBUG"
    }

    os.environ.update(test_vars)

    # Clear the settings cache
    get_settings.cache_clear()

    yield

    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)
    get_settings.cache_clear()


@pytest.fixture(scope="session")
async def setup_test_database(setup_test_settings):
    """Set up the test database at the start of the session."""
    from intellistack.backend.src.main import create_app  # Import locally to avoid early init

    # Create app with test settings
    app = create_app()

    engine = create_async_engine(
        SQLALCHEMY_DATABASE_URL,
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture
async def db_session(setup_test_database):
    """Create a test database session."""
    engine = setup_test_database
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
        await session.rollback()


@pytest.fixture
def client(setup_test_settings):
    """Create a test client for the FastAPI app."""
    from intellistack.backend.src.main import create_app  # Import locally to avoid early init
    app = create_app()
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client for AI-related tests."""
    mock_client = MagicMock()
    mock_client.chat.completions.create = AsyncMock()
    return mock_client


@pytest.fixture
def mock_qdrant_client():
    """Mock Qdrant client for vector store tests."""
    mock_client = MagicMock()
    mock_client.search = AsyncMock()
    mock_client.upload_points = AsyncMock()
    return mock_client