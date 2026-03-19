"""
Unit tests — JWT algorithm enforcement in JWKSAuthMiddleware (Phase 2 / Task 2.3)

Verifies that:
- A token whose header claims alg=RS256 (non-EdDSA) is rejected with
  HTTP 401 and error code INVALID_TOKEN_ALGORITHM before any key lookup.
- A token with alg=EdDSA passes the algorithm gate (key-lookup proceeds).
- Silent continuation on bad algorithm is NOT allowed.
"""
import base64
import json
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi.testclient import TestClient
from fastapi import FastAPI
from fastapi.responses import JSONResponse


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _build_fake_jwt(alg: str, kid: str = "test-kid") -> str:
    """
    Build a structurally valid-looking JWT with the given alg header.
    The signature is fake — we only need the middleware to read the header
    before rejecting based on algorithm.
    """
    header = base64.urlsafe_b64encode(
        json.dumps({"alg": alg, "typ": "JWT", "kid": kid}).encode()
    ).rstrip(b"=").decode()
    payload = base64.urlsafe_b64encode(
        json.dumps({"sub": "user123", "email": "test@example.com"}).encode()
    ).rstrip(b"=").decode()
    signature = base64.urlsafe_b64encode(b"fake_signature").rstrip(b"=").decode()
    return f"{header}.{payload}.{signature}"


def _make_test_app() -> FastAPI:
    """Minimal FastAPI app with JWKSAuthMiddleware for testing."""
    import os
    os.environ.setdefault("SECRET_KEY", "test-secret-key-for-testing-with-32-chars-at-least")
    os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
    os.environ.setdefault("REDIS_URL", "redis://localhost:6379")
    os.environ.setdefault("QDRANT_HOST", "localhost")
    os.environ.setdefault("GOOGLE_REDIRECT_URI", "http://localhost:3000/api/auth/callback/google")
    os.environ.setdefault("GITHUB_REDIRECT_URI", "http://localhost:3000/api/auth/callback/github")
    os.environ.setdefault("BETTER_AUTH_URL", "http://localhost:3001")
    os.environ.setdefault("BETTER_AUTH_JWKS_URL", "http://localhost:3001/.well-known/jwks.json")

    from src.config.settings import get_settings
    get_settings.cache_clear()

    from src.shared.middleware import JWKSAuthMiddleware
    import src.core.auth.jwks as jwks_module
    jwks_module._shared_jwks_manager = None  # reset singleton

    app = FastAPI()

    @app.get("/probe")
    async def probe(request):
        from fastapi import Request
        return {
            "user_id": getattr(request.state, "user_id", None),
            "authed": getattr(request.state, "user", None) is not None,
        }

    # Attach middleware — env vars above already satisfy get_settings();
    # individual tests mock get_shared_jwks_manager at the middleware module level.
    app.add_middleware(JWKSAuthMiddleware)

    return app


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestMiddlewareAlgorithmEnforcement:
    """
    JWKSAuthMiddleware must reject any Bearer token whose JWT header
    claims an algorithm other than EdDSA.
    """

    def test_rs256_token_returns_401(self):
        """RS256-signed tokens must be rejected with HTTP 401."""
        fake_token = _build_fake_jwt(alg="RS256")

        with patch("src.shared.middleware.get_shared_jwks_manager") as mock_mgr:
            mock_instance = MagicMock()
            mock_instance.fetch_jwks = AsyncMock(
                return_value={"keys": [{"kid": "test-kid", "kty": "OKP", "crv": "Ed25519"}]}
            )
            mock_mgr.return_value = mock_instance

            with patch("src.config.settings.get_settings") as mock_settings:
                mock_settings.return_value.better_auth_session_cookie_name = (
                    "better-auth.session_token"
                )
                from src.config.settings import get_settings
                get_settings.cache_clear()

                app = _make_test_app()
                client = TestClient(app, raise_server_exceptions=False)
                response = client.get(
                    "/probe",
                    headers={"Authorization": f"Bearer {fake_token}"},
                )

        assert response.status_code == 401, (
            f"Expected 401 for RS256 token, got {response.status_code}"
        )

    def test_rs256_rejection_returns_structured_error(self):
        """The 401 response body must have code=INVALID_TOKEN_ALGORITHM."""
        fake_token = _build_fake_jwt(alg="RS256")

        with patch("src.shared.middleware.get_shared_jwks_manager") as mock_mgr:
            mock_instance = MagicMock()
            mock_instance.fetch_jwks = AsyncMock(return_value={"keys": []})
            mock_mgr.return_value = mock_instance

            with patch("src.config.settings.get_settings") as mock_settings:
                mock_settings.return_value.better_auth_session_cookie_name = (
                    "better-auth.session_token"
                )
                from src.config.settings import get_settings
                get_settings.cache_clear()

                app = _make_test_app()
                client = TestClient(app, raise_server_exceptions=False)
                response = client.get(
                    "/probe",
                    headers={"Authorization": f"Bearer {fake_token}"},
                )

        assert response.status_code == 401
        body = response.json()
        assert "error" in body
        assert body["error"]["code"] == "INVALID_TOKEN_ALGORITHM"

    def test_hs256_token_returns_401(self):
        """HS256-signed tokens must also be rejected (not just RS256)."""
        fake_token = _build_fake_jwt(alg="HS256")

        with patch("src.shared.middleware.get_shared_jwks_manager") as mock_mgr:
            mock_instance = MagicMock()
            mock_instance.fetch_jwks = AsyncMock(return_value={"keys": []})
            mock_mgr.return_value = mock_instance

            with patch("src.config.settings.get_settings") as mock_settings:
                mock_settings.return_value.better_auth_session_cookie_name = (
                    "better-auth.session_token"
                )
                from src.config.settings import get_settings
                get_settings.cache_clear()

                app = _make_test_app()
                client = TestClient(app, raise_server_exceptions=False)
                response = client.get(
                    "/probe",
                    headers={"Authorization": f"Bearer {fake_token}"},
                )

        assert response.status_code == 401

    def test_none_algorithm_token_returns_401(self):
        """Tokens with alg=none must be rejected — this is the classic bypass attack."""
        fake_token = _build_fake_jwt(alg="none")

        with patch("src.shared.middleware.get_shared_jwks_manager") as mock_mgr:
            mock_instance = MagicMock()
            mock_instance.fetch_jwks = AsyncMock(return_value={"keys": []})
            mock_mgr.return_value = mock_instance

            with patch("src.config.settings.get_settings") as mock_settings:
                mock_settings.return_value.better_auth_session_cookie_name = (
                    "better-auth.session_token"
                )
                from src.config.settings import get_settings
                get_settings.cache_clear()

                app = _make_test_app()
                client = TestClient(app, raise_server_exceptions=False)
                response = client.get(
                    "/probe",
                    headers={"Authorization": f"Bearer {fake_token}"},
                )

        assert response.status_code == 401

    def test_non_eddsa_rejection_includes_www_authenticate_header(self):
        """The 401 must include WWW-Authenticate: Bearer per RFC 6750."""
        fake_token = _build_fake_jwt(alg="RS256")

        with patch("src.shared.middleware.get_shared_jwks_manager") as mock_mgr:
            mock_instance = MagicMock()
            mock_instance.fetch_jwks = AsyncMock(return_value={"keys": []})
            mock_mgr.return_value = mock_instance

            with patch("src.config.settings.get_settings") as mock_settings:
                mock_settings.return_value.better_auth_session_cookie_name = (
                    "better-auth.session_token"
                )
                from src.config.settings import get_settings
                get_settings.cache_clear()

                app = _make_test_app()
                client = TestClient(app, raise_server_exceptions=False)
                response = client.get(
                    "/probe",
                    headers={"Authorization": f"Bearer {fake_token}"},
                )

        assert response.status_code == 401
        assert "www-authenticate" in response.headers or "WWW-Authenticate" in response.headers


class TestMiddlewareAlgorithmPassThrough:
    """EdDSA tokens must pass the algorithm gate and reach key-lookup."""

    def test_eddsa_token_passes_algorithm_gate(self):
        """
        A token claiming alg=EdDSA must NOT receive an INVALID_TOKEN_ALGORITHM
        rejection.  It will fail later (invalid signature) but that is
        a different error path.
        """
        fake_eddsa_token = _build_fake_jwt(alg="EdDSA")

        with patch("src.shared.middleware.get_shared_jwks_manager") as mock_mgr:
            # Return empty key list so key-lookup fails (not algorithm gate)
            mock_instance = MagicMock()
            mock_instance.fetch_jwks = AsyncMock(return_value={"keys": []})
            mock_mgr.return_value = mock_instance

            with patch("src.config.settings.get_settings") as mock_settings:
                mock_settings.return_value.better_auth_session_cookie_name = (
                    "better-auth.session_token"
                )
                from src.config.settings import get_settings
                get_settings.cache_clear()

                app = _make_test_app()
                client = TestClient(app, raise_server_exceptions=False)
                response = client.get(
                    "/probe",
                    headers={"Authorization": f"Bearer {fake_eddsa_token}"},
                )

        # Must NOT be INVALID_TOKEN_ALGORITHM — any other response is fine
        if response.status_code == 401:
            body = response.json()
            assert body.get("error", {}).get("code") != "INVALID_TOKEN_ALGORITHM", (
                "EdDSA tokens must not be rejected at the algorithm gate. "
                "They may fail later for other reasons (e.g., key not found)."
            )
