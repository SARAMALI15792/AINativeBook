import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock
import os
from unittest.mock import patch

from src.config.settings import get_settings
from src.shared.database import Base

# Import all models to ensure they are registered with Base metadata
# This is essential for creating tables during testing
from src.core.auth.models import User, Role, UserRole, Session, OAuthAccount, PasswordResetToken, LoginAttempt  # noqa: F401
from src.core.learning.models import Stage, ContentItem, Badge, Progress, ContentCompletion, UserBadge, Certificate  # noqa: F401
from src.core.content.models import Content, ContentVersion, ContentReview  # noqa: F401
from src.core.content.enhanced_models import ContentHierarchy, ContentVariant, ContentSummary, InteractiveCodeBlock, ContentEngagement, ContentEffectiveness  # noqa: F401
from src.core.institution.models import Institution, InstitutionMember, Cohort, CohortEnrollment, CohortInstructor  # noqa: F401
from src.core.community.models import ForumCategory, ForumThread, ForumPost, ForumReaction, StudyGroup, StudyGroupMember, Mentorship, ModerationRecord  # noqa: F401
from src.core.analytics.models import AnalyticsEvent, CohortAnalytics, InstitutionAnalytics  # noqa: F401
from src.ai.rag.models import RAGConversation, RAGMessage, RAGRetrieval  # noqa: F401
from src.ai.tutor.session_store import TutorSessionItem  # noqa: F401
from src.ai.chatkit.models import ChatKitThread, ChatKitThreadItem, ChatKitRateLimit, AiUsageMetric, AuthEventLog  # noqa: F401
from src.ai.personalization.models import PersonalizationProfile, ChapterPersonalization, TranslationCache  # noqa: F401


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
        "ENVIRONMENT": "development",  # Use development for tests
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
    from src.main import create_app  # Import locally to avoid early init

    # Create app with test settings to initialize components
    # This will trigger the lifespan events which create the tables
    app = create_app()

    # Get the engine from the database module
    from src.shared.database import _engine
    yield _engine
    await _engine.dispose()


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
    from src.main import create_app  # Import locally to avoid early init
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