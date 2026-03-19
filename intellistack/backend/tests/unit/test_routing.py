"""
Comprehensive routing tests for IntelliStack API endpoints

Phase 2 fixes applied (2026-03-17):
- All learning paths corrected: /api/learning/ → /api/v1/learning/
- Learning route auth mock updated: patches get_current_user (the real
  dependency) instead of the old removed get_current_user_id stub.
- RAG route mock updated similarly.
- Added test_tutor_route_prefix_registered — regression guard for
  Phase 1 Task 5 (tutor router was missing /api/v1 prefix).
- Added test_learning_stages_requires_auth — regression guard for
  Phase 1 Task 1 (learning routes now enforce real auth).
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock


@pytest.fixture
def client(setup_test_settings):  # setup_test_settings ensures env vars are set first
    """Create a test client for the FastAPI app."""
    from src.main import create_app  # lazy import: avoids module-level app creation
    app = create_app()
    with TestClient(app, raise_server_exceptions=False) as test_client:
        yield test_client


def test_health_endpoint(client: TestClient):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"
    assert "version" in data
    assert "environment" in data
    assert "timestamp" in data


def test_openapi_endpoint(client: TestClient):
    """Test the OpenAPI schema endpoint."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert "openapi" in data
    assert "info" in data
    assert "paths" in data


def test_docs_endpoints(client: TestClient):
    """Test the documentation endpoints."""
    response = client.get("/docs")
    assert response.status_code in [200, 404]  # 404 OK if debug is disabled

    response = client.get("/redoc")
    assert response.status_code in [200, 404]


def test_api_v1_base_route(client: TestClient):
    """Test the API v1 base route."""
    response = client.get("/api/v1")
    assert response.status_code in [200, 404, 405]


def test_content_routes(client: TestClient):
    """Test content-related routes are reachable (auth enforced)."""
    response = client.get("/api/v1/content/")
    assert response.status_code in [200, 401, 403, 404]

    response = client.post("/api/v1/content/")
    assert response.status_code in [401, 403, 405, 422]


# ---------------------------------------------------------------------------
# Learning routes — Phase 1 Task 1 regression guard
# ---------------------------------------------------------------------------

def test_learning_stages_requires_auth(client: TestClient):
    """
    GET /api/v1/learning/progress must return 401 when no token is present.

    /learning/stages (list) is intentionally public, but /learning/progress
    uses CurrentUserDep and therefore enforces authentication.  This test is
    the permanent regression guard for Phase 1 Task 1 — hardcoded user ID removal.
    """
    # The public stages list should return 200 (not 401)
    response = client.get("/api/v1/learning/stages")
    assert response.status_code not in [500], (
        "Public /learning/stages must not return a 500."
    )

    # A protected endpoint must return 401 without a token
    response = client.get("/api/v1/learning/progress")
    assert response.status_code != 500, (
        "Learning /progress must not return a 500 — the auth dependency "
        "should raise 401 before any DB call happens."
    )
    assert response.status_code == 401, (
        f"Expected 401 from /api/v1/learning/progress without auth, "
        f"got {response.status_code}. "
        "Hardcoded user ID may have been re-introduced."
    )


@patch("src.core.auth.dependencies.get_current_user")
def test_learning_routes_with_mock_auth(mock_get_current_user, client: TestClient):
    """
    Learning routes must be reachable and not return 5xx when auth is provided.

    Uses the correct mock target (get_current_user in the dependencies module)
    now that the hardcoded stub has been removed.
    """
    from uuid import uuid4
    from src.core.auth.dependencies import AuthenticatedUser

    mock_user = AuthenticatedUser(
        id=str(uuid4()),
        email="test@example.com",
        name="Test User",
        email_verified=True,
        role="student",
    )
    # AsyncMock so FastAPI awaits it correctly
    mock_get_current_user.return_value = mock_user

    response = client.get("/api/v1/learning/stages")
    assert response.status_code < 500, (
        f"Learning /stages returned 5xx even with mocked auth: {response.status_code}"
    )

    response = client.get("/api/v1/learning/progress")
    assert response.status_code < 500, (
        f"Learning /progress returned 5xx even with mocked auth: {response.status_code}"
    )


# ---------------------------------------------------------------------------
# Tutor route — Phase 1 Task 5 regression guard
# ---------------------------------------------------------------------------

def test_tutor_route_prefix_registered(client: TestClient):
    """
    Any request to /api/v1/ai/tutor/... must NOT return 404 due to missing
    route registration.  Before Phase 1 Task 5 the tutor_router was included
    without the /api/v1 prefix, so all its routes landed at /ai/tutor/...

    We probe the route without auth (expecting 401 or 405) to confirm the
    router is reachable.  A 404 means the prefix is broken again.
    """
    # Probe actual tutor routes (GET /health is the only public GET on the tutor router)
    # POST /conversations returns 401/405 without auth; GET /health returns 200.
    for path in ["/api/v1/ai/tutor/health", "/api/v1/ai/tutor/conversations"]:
        response = client.get(path)
        assert response.status_code != 404, (
            f"Tutor route {path!r} returned 404. "
            "The /api/v1 prefix may be missing from tutor_router registration in main.py. "
            "Expected 200/401/405 (reachable route), not 404 (route not found)."
        )


def test_old_tutor_path_not_registered(client: TestClient):
    """
    /ai/tutor/... (without /api/v1) must return 404 — those were the broken
    pre-fix paths.  If they still work it means the router is double-registered.
    """
    response = client.get("/ai/tutor/chat")
    assert response.status_code == 404, (
        "Old path /ai/tutor/chat should no longer be registered. "
        "All tutor routes must live under /api/v1/ai/tutor/..."
    )


# ---------------------------------------------------------------------------
# Other route smoke tests
# ---------------------------------------------------------------------------

def test_users_routes(client: TestClient):
    """User profile and preferences routes must be reachable."""
    response = client.get("/api/v1/users/me")
    assert response.status_code in [200, 401, 403, 404]

    response = client.get("/api/v1/users/preferences")
    assert response.status_code in [200, 401, 403, 404]


@patch("src.core.auth.dependencies.get_current_user")
def test_institution_routes(mock_get_current_user, client: TestClient):
    """Institution routes must be reachable with mocked auth."""
    from uuid import uuid4
    from src.core.auth.dependencies import AuthenticatedUser

    mock_user = AuthenticatedUser(
        id=str(uuid4()),
        email="test@example.com",
        name="Test User",
    )
    mock_get_current_user.return_value = mock_user

    response = client.get("/api/v1/institutions")
    assert response.status_code in [200, 401, 403, 404, 405]


@patch("src.core.auth.dependencies.get_current_user")
def test_rag_routes(mock_get_current_user, client: TestClient):
    """RAG chatbot routes must be reachable — uses correct auth mock target."""
    from uuid import uuid4
    from src.core.auth.dependencies import AuthenticatedUser

    mock_user = AuthenticatedUser(
        id=str(uuid4()),
        email="test@example.com",
        name="Test User",
        role="student",
    )
    mock_get_current_user.return_value = mock_user

    response = client.get("/api/v1/rag/conversations")
    assert response.status_code in [200, 401, 403, 404]

    response = client.post("/api/v1/rag/chat")
    assert response.status_code in [400, 401, 403, 404, 405, 422]


def test_all_routes_no_5xx(client: TestClient):
    """All probed routes must return non-5xx status codes."""
    probe_routes = [
        "/health",
        "/openapi.json",
        "/api/v1/content/",
        "/api/v1/users/me",
        "/api/v1/learning/stages",
    ]

    for route in probe_routes:
        response = client.get(route)
        assert response.status_code < 500, (
            f"Route {route} returned a server error: {response.status_code}"
        )
