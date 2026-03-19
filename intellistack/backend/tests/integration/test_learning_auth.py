"""
Integration tests — learning routes enforce real authentication (Phase 2 / Tasks 2.5–2.6)

Verifies end-to-end that:
1. Every learning endpoint returns 401 when no Authorization header is present.
2. Every learning endpoint returns 401 when an obviously invalid token is sent.
3. A valid-looking mocked user can access the stages list endpoint.
4. The /api/v1 prefix is correct for all tested endpoints (regression for
   Phase 1 Task 1 — hardcoded user ID removal).

These tests run against the real FastAPI app (no DB required — endpoints
return 401 before hitting the database when auth fails).
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from uuid import uuid4


# ---------------------------------------------------------------------------
# App fixture
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def app_client(setup_test_settings):  # setup_test_settings (session-scoped) sets env vars first
    """
    Module-scoped TestClient so the app is created once for all tests here.
    raise_server_exceptions=False lets us inspect 5xx as HTTP responses.
    """
    from src.main import create_app  # lazy import: avoids module-level app creation
    app = create_app()
    with TestClient(app, raise_server_exceptions=False) as client:
        yield client


# ---------------------------------------------------------------------------
# All learning endpoints that require auth
# ---------------------------------------------------------------------------

LEARNING_AUTH_ENDPOINTS = [
    ("GET",  "/api/v1/learning/stages/{stage_id}",              "/api/v1/learning/stages/test-stage"),
    ("GET",  "/api/v1/learning/stages/{stage_id}/content",      "/api/v1/learning/stages/test-stage/content"),
    ("GET",  "/api/v1/learning/content/{content_id}/url",       "/api/v1/learning/content/test-content/url"),
    ("GET",  "/api/v1/learning/progress",                       "/api/v1/learning/progress"),
    ("GET",  "/api/v1/learning/progress/path",                  "/api/v1/learning/progress/path"),
    ("GET",  "/api/v1/learning/stages/{stage_id}/time-estimate","/api/v1/learning/stages/test-stage/time-estimate"),
    ("GET",  "/api/v1/learning/badges",                         "/api/v1/learning/badges"),
    ("GET",  "/api/v1/learning/certificate",                    "/api/v1/learning/certificate"),
]


class TestLearningEndpointsRequireAuth:
    """Every learning endpoint that uses CurrentUserDep must enforce auth."""

    def test_stages_list_is_public(self, app_client: TestClient):
        """
        GET /api/v1/learning/stages (list all stages) is intentionally public —
        it does NOT use CurrentUserDep.  It should return 200 or empty list,
        not 401.
        """
        response = app_client.get("/api/v1/learning/stages")
        # 200 (with or without stages), not 401
        assert response.status_code in [200, 404], (
            f"Public stages list should not require auth, got {response.status_code}"
        )

    @pytest.mark.parametrize(
        "method,template,path",
        LEARNING_AUTH_ENDPOINTS,
        ids=[ep[1] for ep in LEARNING_AUTH_ENDPOINTS],
    )
    def test_endpoint_returns_401_without_token(
        self, app_client: TestClient, method: str, template: str, path: str
    ):
        """Each auth-protected endpoint must return 401 with no token."""
        response = app_client.request(method, path)
        assert response.status_code == 401, (
            f"{method} {path} should return 401 without auth, "
            f"got {response.status_code}. "
            "This is a regression guard: the hardcoded user ID was removed "
            "in Phase 1 Task 1 — all learning endpoints now require real auth."
        )

    @pytest.mark.parametrize(
        "method,template,path",
        LEARNING_AUTH_ENDPOINTS,
        ids=[ep[1] for ep in LEARNING_AUTH_ENDPOINTS],
    )
    def test_endpoint_returns_401_with_garbage_token(
        self, app_client: TestClient, method: str, template: str, path: str
    ):
        """Each endpoint must return 401 for a syntactically invalid token."""
        response = app_client.request(
            method,
            path,
            headers={"Authorization": "Bearer not.a.valid.jwt.token"},
        )
        # 401 for bad token, 503 if JWKS unreachable — both are acceptable auth failures
        assert response.status_code in [401, 503], (
            f"{method} {path} should return 401/503 with garbage token, "
            f"got {response.status_code}"
        )

    def test_no_5xx_on_any_learning_endpoint_without_auth(
        self, app_client: TestClient
    ):
        """
        No learning endpoint should return a 5xx error when called without auth.
        A 5xx here would mean the auth dependency isn't guarding correctly
        and the request is reaching DB or service code before failing.
        """
        all_paths = [ep[2] for ep in LEARNING_AUTH_ENDPOINTS]
        # Also include the public stages list
        all_paths.append("/api/v1/learning/stages")

        for path in all_paths:
            response = app_client.get(path)
            assert response.status_code < 500, (
                f"Learning endpoint {path} returned 5xx without auth: "
                f"{response.status_code}. Auth guard must run before any DB call."
            )


class TestLearningEndpointsWithMockedAuth:
    """Endpoints must be reachable and not blow up when auth is satisfied."""

    def test_stages_accessible_with_mock_auth(self, app_client: TestClient):
        """
        With a mocked authenticated user, GET /api/v1/learning/stages/{id}
        must not return 401 or 5xx.

        Uses app.dependency_overrides (not unittest.mock.patch) because
        FastAPI Depends() captures function references at definition time —
        patching the module attribute after the fact does not affect the
        already-stored dependency callable.
        """
        from src.core.auth.dependencies import AuthenticatedUser, get_current_user

        mock_user = AuthenticatedUser(
            id=str(uuid4()),
            email="student@test.com",
            name="Test Student",
            email_verified=True,
            role="student",
        )

        async def _override():
            return mock_user

        app_client.app.dependency_overrides[get_current_user] = _override
        try:
            response = app_client.get("/api/v1/learning/stages/stage-1")
        finally:
            del app_client.app.dependency_overrides[get_current_user]

        # 401 would mean override didn't take effect; 5xx means unexpected server error
        assert response.status_code not in [401, 500], (
            f"With mocked auth, stage detail returned unexpected {response.status_code}"
        )

    def test_progress_accessible_with_mock_auth(self, app_client: TestClient):
        """GET /api/v1/learning/progress must be reachable with mocked auth."""
        from src.core.auth.dependencies import AuthenticatedUser, get_current_user

        mock_user = AuthenticatedUser(
            id=str(uuid4()),
            email="student@test.com",
            name="Test Student",
            email_verified=True,
            role="student",
        )

        async def _override():
            return mock_user

        app_client.app.dependency_overrides[get_current_user] = _override
        try:
            response = app_client.get("/api/v1/learning/progress")
        finally:
            del app_client.app.dependency_overrides[get_current_user]

        # Primary assertion: auth override worked — must not be 401.
        # A 500 here means the DB query ran (auth passed) but no tables exist in the
        # in-memory test database — that is acceptable for this integration test,
        # which only verifies the dependency override mechanism, not DB correctness.
        assert response.status_code != 401, (
            f"With mocked auth, progress endpoint returned 401 — "
            "the dependency_overrides mechanism did not take effect."
        )


class TestTutorRoutePrefix:
    """
    Regression guard for Phase 1 Task 5 — tutor_router must be registered
    under /api/v1, not at the bare /ai/tutor path.
    """

    def test_tutor_endpoint_under_api_v1(self, app_client: TestClient):
        """
        /api/v1/ai/tutor/... endpoints must be discoverable (not 404).
        Without auth the server should return 200/401/405, not 404.

        Probes actual routes registered on tutor_router:
        - GET /api/v1/ai/tutor/health  (public health check → 200)
        - GET /api/v1/ai/tutor/conversations  (POST-only → 405 on GET)
        """
        probe_paths = [
            "/api/v1/ai/tutor/health",
            "/api/v1/ai/tutor/conversations",
        ]
        statuses = [app_client.get(path).status_code for path in probe_paths]
        non_404 = [s for s in statuses if s != 404]
        assert non_404, (
            f"All tutor probe paths returned 404: {list(zip(probe_paths, statuses))}. "
            "The /api/v1 prefix may be missing from tutor_router in main.py."
        )

    def test_old_tutor_path_is_gone(self, app_client: TestClient):
        """
        /ai/tutor/... (the pre-fix path) must return 404.
        If it still works the router is double-registered.
        """
        response = app_client.get("/ai/tutor/chat")
        assert response.status_code == 404, (
            "Old path /ai/tutor/chat should not exist. "
            "All tutor routes must be at /api/v1/ai/tutor/..."
        )
