"""
Unit tests — production CORS guard in Settings (Phase 2 / Task 2.7)

Verifies that:
1. Starting with environment=production and the default localhost-only
   CORS origins raises a ValidationError at startup time.
2. Starting with environment=production AND a real CORS_ORIGINS value
   succeeds without error.
3. The development environment (default) accepts localhost-only origins.
4. The parse_cors_origins validator handles comma-separated strings and
   JSON-array strings correctly.
"""
import os
import pytest
from pydantic import ValidationError


# ---------------------------------------------------------------------------
# Shared env base — all required Settings fields except those being tested
# ---------------------------------------------------------------------------

_BASE_ENV = {
    "SECRET_KEY": "test-secret-key-for-testing-with-32-chars-at-least",
    "DATABASE_URL": "sqlite+aiosqlite:///:memory:",
    "REDIS_URL": "redis://localhost:6379",
    "QDRANT_HOST": "localhost",
    "GOOGLE_REDIRECT_URI": "http://localhost:3000/api/auth/callback/google",
    "GITHUB_REDIRECT_URI": "http://localhost:3000/api/auth/callback/github",
    "BETTER_AUTH_URL": "http://localhost:3001",
    "BETTER_AUTH_JWKS_URL": "http://localhost:3001/.well-known/jwks.json",
    "DEBUG": "False",
    "LOG_LEVEL": "INFO",
}


def _make_settings(extra: dict):
    """
    Import Settings fresh (bypassing lru_cache) with the given env vars.
    Clears the settings cache before and after to avoid cross-test pollution.
    """
    from src.config.settings import get_settings, Settings
    get_settings.cache_clear()

    env = {**_BASE_ENV, **extra}
    original = os.environ.copy()
    os.environ.update(env)
    # Remove keys that extra explicitly sets to None / removes
    for k, v in extra.items():
        if v is None:
            os.environ.pop(k, None)
    try:
        settings = Settings()
    finally:
        os.environ.clear()
        os.environ.update(original)
        get_settings.cache_clear()
    return settings


# ---------------------------------------------------------------------------
# Tests — production guard
# ---------------------------------------------------------------------------

class TestProductionCORSGuard:

    def test_production_with_dev_defaults_raises(self):
        """
        Starting in production with only localhost CORS origins must raise
        a ValidationError so the server never starts with insecure defaults.
        """
        with pytest.raises((ValidationError, ValueError)) as exc_info:
            _make_settings({"ENVIRONMENT": "production"})

        error_text = str(exc_info.value)
        assert "CORS_ORIGINS" in error_text or "production" in error_text.lower(), (
            "The error message should mention CORS_ORIGINS or production environment."
        )

    def test_production_with_real_origins_succeeds(self):
        """
        Production with a real CORS_ORIGINS value must start successfully.
        """
        settings = _make_settings({
            "ENVIRONMENT": "production",
            "CORS_ORIGINS": "https://app.intellistack.io,https://api.intellistack.io",
        })
        assert settings.environment == "production"
        assert "https://app.intellistack.io" in settings.cors_origins

    def test_production_with_single_origin_succeeds(self):
        """A single real HTTPS origin is sufficient to pass the guard."""
        settings = _make_settings({
            "ENVIRONMENT": "production",
            "CORS_ORIGINS": "https://intellistack.io",
        })
        assert "https://intellistack.io" in settings.cors_origins

    def test_development_with_localhost_defaults_succeeds(self):
        """The default localhost-only origins are accepted in development."""
        settings = _make_settings({"ENVIRONMENT": "development"})
        assert settings.environment == "development"
        assert "http://localhost:3000" in settings.cors_origins

    def test_staging_with_localhost_defaults_succeeds(self):
        """Staging is not subject to the production CORS guard."""
        settings = _make_settings({"ENVIRONMENT": "staging"})
        assert settings.environment == "staging"


# ---------------------------------------------------------------------------
# Tests — CORS origins parser
# ---------------------------------------------------------------------------

class TestCORSOriginsParser:

    def test_comma_separated_string_parsed(self):
        """CORS_ORIGINS=a,b,c should produce ['a', 'b', 'c']."""
        settings = _make_settings({
            "CORS_ORIGINS": (
                "https://app.example.com,"
                "https://api.example.com,"
                "http://localhost:3000"
            ),
        })
        assert "https://app.example.com" in settings.cors_origins
        assert "https://api.example.com" in settings.cors_origins
        assert "http://localhost:3000" in settings.cors_origins

    def test_json_array_string_parsed(self):
        """CORS_ORIGINS in JSON-array format must be parsed correctly."""
        settings = _make_settings({
            "CORS_ORIGINS": (
                '["https://app.example.com", "https://api.example.com"]'
            ),
        })
        assert "https://app.example.com" in settings.cors_origins
        assert "https://api.example.com" in settings.cors_origins

    def test_list_passthrough(self):
        """A Python list value is returned as-is."""
        from src.config.settings import Settings
        result = Settings.parse_cors_origins.__func__(
            Settings,
            ["https://a.com", "https://b.com"],
        )
        assert result == ["https://a.com", "https://b.com"]

    def test_whitespace_stripped_from_csv(self):
        """Origins in CSV format must have leading/trailing whitespace stripped."""
        settings = _make_settings({
            "CORS_ORIGINS": " https://a.com , https://b.com ",
        })
        assert "https://a.com" in settings.cors_origins
        assert "https://b.com" in settings.cors_origins
        for origin in settings.cors_origins:
            assert origin == origin.strip(), f"Origin has whitespace: {origin!r}"
