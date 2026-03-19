import pytest
from datetime import datetime, timezone
from unittest.mock import AsyncMock, Mock, patch
import jwt
import httpx

from fastapi import HTTPException, Request
from fastapi.security.http import HTTPAuthorizationCredentials as HTTPAuthCredential

from intellistack.backend.src.core.auth.dependencies import (
    AuthenticatedUser, validate_session_token, sync_user_from_jwt,
    get_current_user, require_role, require_verified_email
)
from intellistack.backend.src.core.auth.models import User
from tests.factories import UserFactory


class TestAuthenticatedUser:
    """Test the AuthenticatedUser dataclass."""

    def test_authenticated_user_creation(self):
        """Test creating an AuthenticatedUser instance."""
        user = AuthenticatedUser(
            id="user123",
            email="test@example.com",
            name="Test User",
            email_verified=True,
            role="student"
        )

        assert user.id == "user123"
        assert user.email == "test@example.com"
        assert user.name == "Test User"
        assert user.email_verified is True
        assert user.role == "student"


class TestValidateSessionToken:
    """Test the validate_session_token function."""

    @pytest.mark.asyncio
    async def test_validate_session_token_success(self):
        """Test validating a valid session token."""
        # Mock the HTTP client response
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "user": {
                "id": "user123",
                "email": "test@example.com",
                "name": "Test User",
                "emailVerified": True,
                "role": "student"
            }
        }

        mock_client = AsyncMock()
        mock_client.get.return_value.__aenter__.return_value = mock_response
        mock_client.get.return_value.__aexit__.return_value = Mock()

        with patch('intellistack.backend.src.core.auth.dependencies.httpx.AsyncClient') as mock_httpx:
            mock_httpx.return_value = mock_client
            with patch('intellistack.backend.src.core.auth.dependencies.get_settings') as mock_settings:
                mock_settings.return_value.better_auth_jwks_url = "https://auth.example.com/.well-known/jwks.json"
                mock_settings.return_value.better_auth_session_cookie_name = "authjs.session-token"

                result = await validate_session_token("valid_session_token")

        assert isinstance(result, AuthenticatedUser)
        assert result.id == "user123"
        assert result.email == "test@example.com"
        assert result.name == "Test User"
        assert result.email_verified is True
        assert result.role == "student"

    @pytest.mark.asyncio
    async def test_validate_session_token_invalid_response(self):
        """Test validating an invalid session token."""
        # Mock the HTTP client response
        mock_response = AsyncMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {}

        mock_client = AsyncMock()
        mock_client.get.return_value.__aenter__.return_value = mock_response
        mock_client.get.return_value.__aexit__.return_value = Mock()

        with patch('intellistack.backend.src.core.auth.dependencies.httpx.AsyncClient') as mock_httpx:
            mock_httpx.return_value = mock_client
            with patch('intellistack.backend.src.core.auth.dependencies.get_settings') as mock_settings:
                mock_settings.return_value.better_auth_jwks_url = "https://auth.example.com/.well-known/jwks.json"
                mock_settings.return_value.better_auth_session_cookie_name = "authjs.session-token"

                result = await validate_session_token("invalid_session_token")

        assert result is None

    @pytest.mark.asyncio
    async def test_validate_session_token_exception(self):
        """Test handling exception during session validation."""
        mock_client = AsyncMock()
        mock_client.get.side_effect = Exception("Network error")

        with patch('intellistack.backend.src.core.auth.dependencies.httpx.AsyncClient') as mock_httpx:
            mock_httpx.return_value = mock_client
            with patch('intellistack.backend.src.core.auth.dependencies.get_settings') as mock_settings:
                mock_settings.return_value.better_auth_jwks_url = "https://auth.example.com/.well-known/jwks.json"
                mock_settings.return_value.better_auth_session_cookie_name = "authjs.session-token"

                result = await validate_session_token("valid_session_token")

        assert result is None


class TestSyncUserFromJWT:
    """Test the sync_user_from_jwt function."""

    @pytest.mark.asyncio
    async def test_sync_user_new_user(self, db_session):
        """Test syncing a new user from JWT claims."""
        user_id = "user123"
        email = "test@example.com"
        name = "Test User"
        email_verified = True
        role = "student"

        # Verify user doesn't exist initially
        from sqlalchemy import select
        result = await db_session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        assert user is None

        # Now sync the user
        await sync_user_from_jwt(user_id, email, name, email_verified, role, db_session)

        # Check that user was created
        result = await db_session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()

        assert user is not None
        assert user.id == user_id
        assert user.email == email
        assert user.name == name
        assert user.email_verified == email_verified
        assert user.role == role


    @pytest.mark.asyncio
    async def test_sync_user_existing_user(self, db_session):
        """Test syncing an existing user updates their info."""
        # Create existing user
        existing_user = UserFactory(
            id="user123",
            email="old@example.com",
            name="Old Name",
            email_verified=False,
            role="student"
        )
        db_session.add(existing_user)
        await db_session.commit()

        # Sync with new info
        await sync_user_from_jwt(
            "user123",
            "new@example.com",
            "New Name",
            True,
            "instructor",
            db_session
        )

        # Refresh and check updates
        await db_session.refresh(existing_user)

        assert existing_user.email == "new@example.com"
        assert existing_user.name == "New Name"
        assert existing_user.email_verified is True
        assert existing_user.role == "instructor"


class TestGetCurrentUser:
    """Test the get_current_user dependency."""

    @pytest.mark.asyncio
    async def test_get_current_user_from_request_state(self, db_session):
        """Test getting user from request.state (middleware validated)."""
        # Create mock request with user in state
        request = Request({"type": "http", "method": "GET", "path": "/test"})
        request._url = "http://testserver/test"
        request.state = Mock()
        request.state.user = {
            "id": "user123",
            "email": "test@example.com",
            "name": "Test User",
            "email_verified": True,
            "role": "student"
        }

        user = await get_current_user(request, None, db_session)

        assert isinstance(user, AuthenticatedUser)
        assert user.id == "user123"
        assert user.email == "test@example.com"
        assert user.name == "Test User"
        assert user.email_verified is True
        assert user.role == "student"

    @pytest.mark.asyncio
    async def test_get_current_user_no_token(self, db_session):
        """Test getting user with no token raises 401."""
        request = Request({"type": "http", "method": "GET", "path": "/test"})
        request._url = "http://testserver/test"
        request.state = Mock()
        request.state.user = None

        credentials = None

        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(request, credentials, db_session)

        assert exc_info.value.status_code == 401
        assert "Missing authorization token" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_get_current_user_jwt_valid(self, db_session):
        """Test getting user with valid JWT token."""
        # Create a valid JWT token
        payload = {
            "sub": "user123",
            "email": "test@example.com",
            "name": "Test User",
            "email_verified": True,
            "role": "student",
            "iat": int(datetime.now(timezone.utc).timestamp()),
            "exp": int((datetime.now(timezone.utc) + datetime.timedelta(hours=1)).timestamp())
        }
        token = jwt.encode(payload, "secret", algorithm="HS256")

        # Mock the JWKS manager
        mock_jwks_manager = AsyncMock()
        mock_jwks_manager.fetch_jwks.return_value = {
            "keys": [
                {
                    "kty": "oct",
                    "use": "sig",
                    "k": jwt.algorithms.HMACAlgorithm.to_jwk("secret")["k"],
                    "alg": "HS256",
                    "kid": "test-key"
                }
            ]
        }

        with patch('intellistack.backend.src.core.auth.dependencies.get_jwks_manager') as mock_get_jwks:
            mock_get_jwks.return_value = mock_jwks_manager

            with patch('intellistack.backend.src.core.auth.dependencies.get_settings') as mock_settings:
                mock_settings.return_value.better_auth_jwks_url = "https://auth.example.com/.well-known/jwks.json"
                mock_settings.return_value.better_auth_session_cookie_name = "authjs.session-token"
                mock_settings.return_value.better_auth_audience = None
                mock_settings.return_value.better_auth_issuer = None

                # Create request with JWT token
                request = Request({"type": "http", "method": "GET", "path": "/test"})
                request._url = "http://testserver/test"
                request.state = Mock()
                request.state.user = None
                request.cookies = {}

                # Create credentials with JWT token
                credentials = HTTPAuthCredential(scheme="Bearer", credentials=token)

                user = await get_current_user(request, credentials, db_session)

                assert isinstance(user, AuthenticatedUser)
                assert user.id == "user123"
                assert user.email == "test@example.com"
                assert user.name == "Test User"
                assert user.email_verified is True
                assert user.role == "student"


class TestRequireRole:
    """Test the require_role dependency."""

    @pytest.mark.asyncio
    async def test_require_role_success(self):
        """Test requiring role when user has the role."""
        user = AuthenticatedUser(
            id="user123",
            email="test@example.com",
            role="admin"
        )

        # Create role check dependency for admin
        role_check = require_role("admin", "instructor")

        # Mock the get_current_user dependency
        with patch('intellistack.backend.src.core.auth.dependencies.get_current_user', return_value=user):
            result = await role_check()

        assert result == user

    @pytest.mark.asyncio
    async def test_require_role_forbidden(self):
        """Test requiring role when user doesn't have the role."""
        user = AuthenticatedUser(
            id="user123",
            email="test@example.com",
            role="student"  # Not admin or instructor
        )

        # Create role check dependency for admin/instructor
        role_check = require_role("admin", "instructor")

        # Mock the get_current_user dependency
        with patch('intellistack.backend.src.core.auth.dependencies.get_current_user', return_value=user):
            with pytest.raises(HTTPException) as exc_info:
                await role_check()

        assert exc_info.value.status_code == 403
        assert "requires one of these roles" in exc_info.value.detail


class TestRequireVerifiedEmail:
    """Test the require_verified_email dependency."""

    @pytest.mark.asyncio
    async def test_require_verified_email_success(self):
        """Test requiring verified email when email is verified."""
        user = AuthenticatedUser(
            id="user123",
            email="test@example.com",
            email_verified=True
        )

        # Mock the get_current_user dependency
        with patch('intellistack.backend.src.core.auth.dependencies.get_current_user', return_value=user):
            result = await require_verified_email(user)

        assert result == user

    @pytest.mark.asyncio
    async def test_require_verified_email_forbidden(self):
        """Test requiring verified email when email is not verified."""
        user = AuthenticatedUser(
            id="user123",
            email="test@example.com",
            email_verified=False
        )

        # Mock the get_current_user dependency
        with patch('intellistack.backend.src.core.auth.dependencies.get_current_user', return_value=user):
            with pytest.raises(HTTPException) as exc_info:
                await require_verified_email(user)

        assert exc_info.value.status_code == 403
        assert "Email verification required" in exc_info.value.detail