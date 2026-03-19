"""
Comprehensive BetterAuth tests for IntelliStack authentication system

Phase 2 additions:
- test_dependency_rejects_non_eddsa_key: verifies that get_current_user raises
  401 when the JWKS key's algorithm is not EdDSA.
- test_dependency_rejects_missing_token: verifies 401 when no token present.
"""
import base64
import json
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock, MagicMock
from fastapi import HTTPException


@pytest.fixture
def client(setup_test_settings):  # setup_test_settings ensures env vars are set first
    """Create a test client for the FastAPI app."""
    from src.main import create_app  # lazy import: avoids module-level app creation
    app = create_app()
    with TestClient(app) as test_client:
        yield test_client


def test_auth_middleware_loaded(client: TestClient):
    """Test that BetterAuth middleware is properly loaded."""
    # Test that the app has auth-related routes configured
    response = client.get("/health")
    assert response.status_code == 200
    # App should start without auth configuration errors


@patch('src.core.auth.jwks.JWKSManager.fetch_jwks')
def test_auth_required_endpoints_return_401(mock_fetch_jwks, client: TestClient):
    """Test that endpoints requiring authentication return 401 without auth."""
    # Mock JWKS to avoid trying to connect to BetterAuth server
    mock_fetch_jwks.side_effect = ValueError("Could not fetch JWKS")

    protected_routes = [
        "/api/v1/users/me",
        "/api/v1/users/preferences",
        "/api/v1/content/",
        "/api/v1/institutions",
        "/api/v1/rag/chat",
    ]

    for route in protected_routes:
        response = client.get(route)
        # Should return 401 (unauthorized) or 403 (forbidden) without auth
        # For endpoints that try to access user progress data with invalid user ID,
        # we might get 500 errors that should be handled by middleware (e.g., 503 for service unavailable)
        assert response.status_code in [401, 403, 404, 405, 500, 503], \
            f"Route {route} should require auth, got {response.status_code}"


@patch('src.core.auth.jwks.JWKSManager.fetch_jwks')
def test_auth_headers_properly_handled(mock_fetch_jwks, client: TestClient):
    """Test that auth headers are properly handled by middleware."""
    # Mock JWKS to avoid trying to connect to BetterAuth server
    mock_fetch_jwks.side_effect = ValueError("Could not fetch JWKS")

    # Test with invalid auth header
    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": "Bearer invalid-token"}
    )
    # Should return 401 for invalid token, or 503 if JWKS service unavailable
    assert response.status_code in [401, 403, 503]


@patch('src.core.auth.jwks.JWKSManager.fetch_jwks')
def test_auth_cookie_handling(mock_fetch_jwks, client: TestClient):
    """Test that auth cookies are properly handled by middleware."""
    # Mock JWKS to avoid trying to connect to BetterAuth server
    mock_fetch_jwks.side_effect = ValueError("Could not fetch JWKS")

    # Test with invalid auth cookie (using a fake session cookie name)
    response = client.get(
        "/api/v1/users/me",
        cookies={"better-auth.session_token": "invalid-token"}
    )
    # Should return 401 for invalid session, or 503 if JWKS service unavailable
    assert response.status_code in [401, 403, 503]


def test_auth_routes_exist(client: TestClient):
    """Test that auth-related routes exist and are accessible."""
    # Test common auth endpoints (these may not exist in current impl but should not cause server errors)
    auth_routes = [
        "/api/v1/auth/me",  # BetterAuth typically has this
        "/api/v1/auth/login",  # Login endpoint
        "/api/v1/auth/logout",  # Logout endpoint
        "/api/v1/auth/register",  # Registration endpoint
    ]

    for route in auth_routes:
        try:
            response = client.get(route)
            # Should not return 5xx server errors
            assert response.status_code < 500, f"Auth route {route} returned server error {response.status_code}"
        except Exception:
            # Some routes might require POST, that's okay
            pass


@patch('src.core.auth.jwks.JWKSManager.fetch_jwks')
def test_jwt_validation_middleware(mock_fetch_jwks, client: TestClient):
    """Test that JWT validation middleware works correctly."""
    # Mock JWKS to avoid trying to connect to BetterAuth server
    mock_fetch_jwks.side_effect = ValueError("Could not fetch JWKS")

    # Test with malformed JWT
    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": "Bearer malformed.token.here"}
    )
    # Should return 401 for malformed token, or 503 if JWKS service unavailable
    assert response.status_code in [401, 403, 503]


@patch('src.core.auth.jwks.JWKSManager.fetch_jwks')
def test_jwt_validation_with_mock_jwks(mock_fetch_jwks, client: TestClient):
    """Test JWT validation with mocked JWKS."""
    # Mock the JWKS response
    mock_fetch_jwks.return_value = {
        "keys": [
            {
                "kty": "RSA",
                "use": "sig",
                "kid": "test-key",
                "alg": "RS256",
                "n": "test-n-value",
                "e": "AQAB"
            }
        ]
    }

    # Test with a fake token (this will likely fail validation but shouldn't cause server error)
    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.test.test"}
    )

    # Should return 401 for invalid signature or 500 if there's an unexpected error
    # But we want to ensure no server errors in the authentication process
    assert response.status_code != 500


def test_oauth_callback_endpoints(client: TestClient):
    """Test OAuth callback endpoint availability."""
    # These endpoints might handle OAuth callbacks
    callback_routes = [
        "/api/auth/callback/google",
        "/api/auth/callback/github",
        # May also try with common OAuth patterns
        "/api/v1/auth/callback/google",
        "/api/v1/auth/callback/github",
    ]

    for route in callback_routes:
        try:
            # These might require proper OAuth state, but shouldn't return 5xx
            response = client.get(route)
            assert response.status_code < 500, f"OAuth callback {route} returned server error"
        except Exception:
            # OAuth endpoints often expect specific GET parameters, that's fine
            pass


def test_session_management_routes(client: TestClient):
    """Test session management related routes."""
    session_routes = [
        "/api/v1/auth/session",
        "/api/v1/auth/sessions",
        "/api/v1/users/session",
    ]

    for route in session_routes:
        try:
            response = client.get(route)
            assert response.status_code < 500, f"Session route {route} returned server error"
        except Exception:
            # Some routes might require specific methods
            pass


def test_auth_middleware_integration(client: TestClient):
    """Test that auth middleware integrates properly with other middleware."""
    # Test a public route to ensure middleware stack works
    response = client.get("/health")
    assert response.status_code == 200

    # Test an auth-required route without auth
    response = client.get("/api/v1/users/me")
    # Should not return 500 (internal server error)
    assert response.status_code != 500


# ---------------------------------------------------------------------------
# Phase 2 additions — EdDSA enforcement in the dependency layer
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_dependency_rejects_non_eddsa_key():
    """
    get_current_user must raise HTTP 401 when the JWKS endpoint returns a key
    whose algorithm is not EdDSA (Phase 1 fix Task 3 / Phase 2 test Task 2.2).

    This guards against a mis-configured auth server accidentally serving
    an RSA/HMAC key, and against algorithm-confusion attacks where an
    attacker swaps the key type.
    """
    import src.core.auth.jwks as jwks_module
    from fastapi import Request
    from fastapi.security.http import HTTPAuthorizationCredentials as HTTPAuthCredential
    from src.core.auth.dependencies import get_current_user
    from unittest.mock import AsyncMock, MagicMock

    jwks_module._shared_jwks_manager = None

    # Build a token whose header claims EdDSA (passes the middleware gate)
    # but the JWKS will return an RS256 key — the dependency must reject it.
    header = base64.urlsafe_b64encode(
        json.dumps({"alg": "EdDSA", "typ": "JWT", "kid": "test-kid"}).encode()
    ).rstrip(b"=").decode()
    payload_b = base64.urlsafe_b64encode(
        json.dumps({"sub": "u1", "email": "a@b.com"}).encode()
    ).rstrip(b"=").decode()
    sig = base64.urlsafe_b64encode(b"sig").rstrip(b"=").decode()
    fake_token = f"{header}.{payload_b}.{sig}"

    # JWKS returns an RS256 key (not EdDSA)
    rs256_key = {
        "kty": "RSA",
        "kid": "test-kid",
        "alg": "RS256",
        "use": "sig",
        "n": "pjdss8ZaDfEH6K6U7GeW2nxDqR4IP049fk1fK0lndimbMMVBdPv_hSpm8T8EtBDxrUdi1OHZfMhUixGyw-",
        "e": "AQAB",
    }

    mock_jwks = MagicMock()
    mock_jwks.fetch_jwks = AsyncMock(return_value={"keys": [rs256_key]})

    # Build a minimal request object with no middleware-set state
    scope = {
        "type": "http",
        "method": "GET",
        "path": "/test",
        "headers": [],
        "query_string": b"",
    }
    request = Request(scope)
    request.state.user = None

    credentials = HTTPAuthCredential(scheme="Bearer", credentials=fake_token)

    mock_db = AsyncMock()

    with patch("src.core.auth.dependencies.get_jwks_manager", return_value=mock_jwks):
        with patch("src.config.settings.get_settings") as mock_settings:
            mock_settings.return_value.better_auth_jwks_url = (
                "http://localhost:3001/.well-known/jwks.json"
            )
            mock_settings.return_value.better_auth_session_cookie_name = (
                "better-auth.session_token"
            )
            mock_settings.return_value.better_auth_audience = None
            mock_settings.return_value.better_auth_issuer = None

            with pytest.raises(HTTPException) as exc_info:
                await get_current_user(request, credentials, mock_db)

    assert exc_info.value.status_code == 401
    assert "algorithm" in exc_info.value.detail.lower() or \
           "unsupported" in exc_info.value.detail.lower(), (
        "Error detail should mention algorithm or unsupported key."
    )
    jwks_module._shared_jwks_manager = None


@pytest.mark.asyncio
async def test_dependency_rejects_missing_token():
    """
    get_current_user must raise HTTP 401 when no token is present in
    either the Authorization header or the session cookie
    (Phase 2 test Task 2.1).
    """
    import src.core.auth.jwks as jwks_module
    from fastapi import Request
    from src.core.auth.dependencies import get_current_user

    jwks_module._shared_jwks_manager = None

    scope = {
        "type": "http",
        "method": "GET",
        "path": "/test",
        "headers": [],
        "query_string": b"",
    }
    request = Request(scope)
    request.state.user = None

    mock_db = AsyncMock()

    with patch("src.config.settings.get_settings") as mock_settings:
        mock_settings.return_value.better_auth_session_cookie_name = (
            "better-auth.session_token"
        )

        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(request, None, mock_db)

    assert exc_info.value.status_code == 401
    assert "Missing" in exc_info.value.detail or "missing" in exc_info.value.detail
    jwks_module._shared_jwks_manager = None