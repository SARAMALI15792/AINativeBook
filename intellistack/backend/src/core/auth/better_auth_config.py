"""
BetterAuth-compatible configuration and utilities for IntelliStack platform.

This module provides a custom implementation that is compatible with BetterAuth's
JavaScript SDK on the frontend, using standard Python authentication libraries:
- python-jose for JWT handling
- authlib for OAuth2 flows
- passlib for password hashing (via service.py)
"""
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Optional, List
from functools import lru_cache

from jose import JWTError, jwt
from jose.constants import ALGORITHMS
from authlib.integrations.httpx_client import AsyncOAuth2Client
from authlib.oauth2.rfc6749 import OAuth2Error

from src.config.settings import get_settings
from src.config.logging import get_logger

logger = get_logger(__name__)


class BetterAuthConfig:
    """
    Configuration for BetterAuth-compatible authentication.

    Provides settings for:
    - JWT token generation and validation
    - Session management
    - OAuth provider configuration
    - Rate limiting settings
    """

    def __init__(self):
        settings = get_settings()
        self.secret_key = settings.secret_key
        self.algorithm = settings.algorithm  # HS256
        self.access_token_expire_minutes = settings.access_token_expire_minutes
        self.refresh_token_expire_days = settings.refresh_token_expire_days
        self.base_url = f"http://{settings.host}:{settings.port}"

        # Cookie settings for BetterAuth compatibility
        self.cookie_name = "intellistack.session"
        self.cookie_secure = settings.environment == "production"
        self.cookie_http_only = True
        self.cookie_same_site = "lax"
        self.cookie_max_age_days = 7

        # Rate limiting
        self.rate_limit_enabled = True
        self.rate_limit_window = 60  # seconds
        self.rate_limit_max_requests = 10

        # OAuth providers (configured via environment variables)
        self.oauth_providers: Dict[str, Dict[str, str]] = {}

        # Google OAuth
        google_client_id = getattr(settings, 'google_client_id', None)
        google_client_secret = getattr(settings, 'google_client_secret', None)
        if google_client_id and google_client_secret:
            self.oauth_providers["google"] = {
                "client_id": google_client_id,
                "client_secret": google_client_secret,
                "authorize_url": "https://accounts.google.com/o/oauth2/v2/auth",
                "token_url": "https://oauth2.googleapis.com/token",
                "userinfo_url": "https://www.googleapis.com/oauth2/v2/userinfo",
                "redirect_uri": f"{self.base_url}/api/v1/auth/callback/google",
                "scope": "openid email profile",
            }

        # GitHub OAuth
        github_client_id = getattr(settings, 'github_client_id', None)
        github_client_secret = getattr(settings, 'github_client_secret', None)
        if github_client_id and github_client_secret:
            self.oauth_providers["github"] = {
                "client_id": github_client_id,
                "client_secret": github_client_secret,
                "authorize_url": "https://github.com/login/oauth/authorize",
                "token_url": "https://github.com/login/oauth/access_token",
                "userinfo_url": "https://api.github.com/user",
                "redirect_uri": f"{self.base_url}/api/v1/auth/callback/github",
                "scope": "read:user user:email",
            }

    def create_access_token(
        self,
        user_id: str,
        email: str,
        roles: List[str],
        additional_claims: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Create a JWT access token compatible with BetterAuth format."""
        now = datetime.now(timezone.utc)
        expires = now + timedelta(minutes=self.access_token_expire_minutes)

        payload = {
            "sub": str(user_id),  # Subject (user ID)
            "userId": str(user_id),  # BetterAuth compatibility
            "email": email,
            "roles": roles,
            "iat": now,  # Issued at
            "exp": expires,  # Expiration
            "type": "access",
        }

        if additional_claims:
            payload.update(additional_claims)

        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def create_session_token(
        self,
        user_id: str,
        session_id: str,
        expires_days: Optional[int] = None,
    ) -> str:
        """Create a session token for cookie-based auth (BetterAuth style)."""
        now = datetime.now(timezone.utc)
        expires = now + timedelta(days=expires_days or self.cookie_max_age_days)

        payload = {
            "sub": str(user_id),
            "userId": str(user_id),
            "sessionId": session_id,
            "iat": now,
            "exp": expires,
            "type": "session",
        }

        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def decode_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Decode and validate a JWT token."""
        try:
            payload = jwt.decode(
                token, self.secret_key, algorithms=[self.algorithm]
            )
            return payload
        except JWTError as e:
            logger.warning("Token validation failed", error=str(e))
            return None
        except Exception as e:
            logger.error("Unexpected token error", error=str(e))
            return None

    def get_oauth_client(self, provider: str) -> Optional[AsyncOAuth2Client]:
        """Get an OAuth2 client for a specific provider."""
        if provider not in self.oauth_providers:
            return None

        config = self.oauth_providers[provider]
        return AsyncOAuth2Client(
            client_id=config["client_id"],
            client_secret=config["client_secret"],
            scope=config.get("scope"),
            redirect_uri=config["redirect_uri"],
        )


@lru_cache
def get_better_auth_config() -> BetterAuthConfig:
    """Get cached BetterAuth configuration instance."""
    return BetterAuthConfig()


# Global instance for import convenience
better_auth = get_better_auth_config()
