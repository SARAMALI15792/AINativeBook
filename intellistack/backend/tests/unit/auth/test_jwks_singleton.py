"""
Unit tests — shared JWKS manager singleton (Phase 2 / Task 2.4)

Verifies that get_shared_jwks_manager() always returns the same
JWKSManager instance so both middleware and the dependency layer share
a single cache, backoff counter, and fetch lifecycle.
"""
import pytest
from unittest.mock import patch, MagicMock

import src.core.auth.jwks as jwks_module
from src.core.auth.jwks import JWKSManager, get_shared_jwks_manager


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _reset_singleton():
    """Reset the module-level singleton and settings cache between tests."""
    jwks_module._shared_jwks_manager = None
    from src.config.settings import get_settings
    get_settings.cache_clear()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestSharedJWKSSingleton:
    """get_shared_jwks_manager must return the same instance on every call."""

    def test_returns_jwks_manager_instance(self):
        """Return value must be a JWKSManager."""
        _reset_singleton()
        with patch("src.config.settings.get_settings") as mock_settings:
            mock_settings.return_value.better_auth_jwks_url = (
                "http://localhost:3001/.well-known/jwks.json"
            )
            instance = get_shared_jwks_manager()

        assert isinstance(instance, JWKSManager)
        _reset_singleton()

    def test_same_instance_returned_on_second_call(self):
        """Two consecutive calls must return the identical object."""
        _reset_singleton()
        with patch("src.config.settings.get_settings") as mock_settings:
            mock_settings.return_value.better_auth_jwks_url = (
                "http://localhost:3001/.well-known/jwks.json"
            )
            first = get_shared_jwks_manager()
            second = get_shared_jwks_manager()

        assert first is second, (
            "get_shared_jwks_manager() must return the same object "
            "on every call — both middleware and the dependency layer "
            "must share a single JWKS cache."
        )
        _reset_singleton()

    def test_settings_fetched_only_once(self):
        """Settings must be read exactly once even after multiple calls."""
        _reset_singleton()
        with patch("src.config.settings.get_settings") as mock_settings:
            mock_settings.return_value.better_auth_jwks_url = (
                "http://localhost:3001/.well-known/jwks.json"
            )
            get_shared_jwks_manager()
            get_shared_jwks_manager()
            get_shared_jwks_manager()

        # get_settings() was called once during the first call; subsequent
        # calls skip the if-branch entirely.
        assert mock_settings.call_count == 1
        _reset_singleton()

    def test_singleton_uses_configured_jwks_url(self):
        """The manager must be initialised with the URL from settings."""
        _reset_singleton()
        expected_url = "https://auth.example.com/.well-known/jwks.json"
        with patch("src.config.settings.get_settings") as mock_settings:
            mock_settings.return_value.better_auth_jwks_url = expected_url
            instance = get_shared_jwks_manager()

        assert instance.jwks_url == expected_url
        _reset_singleton()

    def test_middleware_and_dependency_share_instance(self):
        """
        Simulate what happens at startup: middleware creates its reference,
        then the dependency layer creates its reference.  Both must hold
        the same object.
        """
        _reset_singleton()
        with patch("src.config.settings.get_settings") as mock_settings:
            mock_settings.return_value.better_auth_jwks_url = (
                "http://localhost:3001/.well-known/jwks.json"
            )
            # Middleware init path
            middleware_ref = get_shared_jwks_manager()
            # Dependency init path
            dependency_ref = get_shared_jwks_manager()

        assert middleware_ref is dependency_ref
        # Dirty the cache on one side and verify the other sees the change
        middleware_ref.backoff_attempts = 99
        assert dependency_ref.backoff_attempts == 99, (
            "Cache state must be shared: if middleware increments "
            "backoff_attempts the dependency layer must observe the same value."
        )
        _reset_singleton()
