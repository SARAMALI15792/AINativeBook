"""JWKS (JSON Web Key Set) Manager for Better-Auth JWT validation.

Fetches and caches public keys from Better-Auth OIDC server's JWKS endpoint.
Allows FastAPI to validate JWT tokens without calling auth server per request.

Features:
- Caches JWKS with 5-minute TTL
- Falls back to last-known-good keys if endpoint unreachable
- Implements exponential backoff for failed requests
"""

import asyncio
import httpx
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from functools import lru_cache

logger = logging.getLogger(__name__)


class JWKSManager:
    """Manages JWKS caching and retrieval from Better-Auth server."""

    def __init__(self, jwks_url: str, cache_ttl_minutes: int = 5):
        """
        Initialize JWKS manager.

        Args:
            jwks_url: URL to Better-Auth JWKS endpoint (/.well-known/jwks.json)
            cache_ttl_minutes: Cache time-to-live in minutes
        """
        self.jwks_url = jwks_url
        self.cache_ttl = timedelta(minutes=cache_ttl_minutes)
        self.cached_jwks: Optional[Dict[str, Any]] = None
        self.cache_time: Optional[datetime] = None
        self.last_known_good_jwks: Optional[Dict[str, Any]] = None
        self.backoff_until: Optional[datetime] = None
        self.backoff_attempts = 0
        self.max_backoff_attempts = 3

    def _is_cache_valid(self) -> bool:
        """Check if cached JWKS is still valid."""
        if not self.cached_jwks or not self.cache_time:
            return False
        return datetime.utcnow() < self.cache_time + self.cache_ttl

    def _is_backoff_active(self) -> bool:
        """Check if we're in backoff period."""
        if not self.backoff_until:
            return False
        if datetime.utcnow() < self.backoff_until:
            return True
        # Backoff period expired
        self.backoff_until = None
        self.backoff_attempts = 0
        return False

    def _calculate_backoff_delay(self) -> int:
        """Calculate exponential backoff delay in seconds."""
        # 2^attempt seconds: 2s, 4s, 8s
        return min(2 ** self.backoff_attempts, 60)

    async def fetch_jwks(self) -> Dict[str, Any]:
        """
        Fetch JWKS from Better-Auth server with caching and fallback.

        Returns:
            JWKS dictionary with 'keys' array

        Raises:
            ValueError: If JWKS cannot be fetched and no fallback available
        """
        # Return cached if valid
        if self._is_cache_valid() and self.cached_jwks:
            logger.debug(f"JWKS cache hit (expires in {(self.cache_time + self.cache_ttl - datetime.utcnow()).seconds}s)")
            return self.cached_jwks

        # If in backoff, return last known good
        if self._is_backoff_active():
            if self.last_known_good_jwks:
                logger.warning(
                    f"JWKS endpoint in backoff (attempt {self.backoff_attempts}/{self.max_backoff_attempts}), "
                    f"using last known good keys"
                )
                return self.last_known_good_jwks
            raise ValueError("JWKS endpoint unreachable and no cached keys available")

        try:
            # Fetch from endpoint
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(self.jwks_url)
                response.raise_for_status()

            jwks = response.json()

            # Validate response has 'keys' array
            if "keys" not in jwks or not isinstance(jwks["keys"], list):
                raise ValueError("Invalid JWKS response: missing 'keys' array")

            # Cache the result
            self.cached_jwks = jwks
            self.cache_time = datetime.utcnow()
            self.last_known_good_jwks = jwks  # Update fallback
            self.backoff_attempts = 0  # Reset backoff counter

            logger.info(f"✅ JWKS fetched successfully ({len(jwks['keys'])} keys)")
            return jwks

        except httpx.HTTPError as e:
            logger.error(f"Failed to fetch JWKS: {e}")

            # Increase backoff attempts
            self.backoff_attempts += 1

            # Calculate backoff delay
            delay = self._calculate_backoff_delay()
            self.backoff_until = datetime.utcnow() + timedelta(seconds=delay)

            if self.backoff_attempts >= self.max_backoff_attempts:
                logger.critical(
                    f"JWKS fetch failed {self.max_backoff_attempts} times. "
                    f"Will retry after {delay}s."
                )

            # Return last known good or raise
            if self.last_known_good_jwks:
                logger.warning(f"Using last known good JWKS (from {self.cache_time})")
                return self.last_known_good_jwks

            raise ValueError(
                f"Cannot fetch JWKS from {self.jwks_url}: {e}. "
                f"No cached keys available."
            )

        except Exception as e:
            logger.error(f"Unexpected error fetching JWKS: {e}")
            if self.last_known_good_jwks:
                logger.warning("Using last known good JWKS")
                return self.last_known_good_jwks
            raise

    @lru_cache(maxsize=1)
    def get_jwks_sync(self) -> Dict[str, Any]:
        """
        Synchronous JWKS getter (uses cached value, doesn't fetch).

        Returns:
            Cached JWKS dictionary or raises if not available
        """
        if self.cached_jwks:
            return self.cached_jwks
        if self.last_known_good_jwks:
            return self.last_known_good_jwks
        raise ValueError("No JWKS data available")

    async def get_key(self, kid: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific key from JWKS by key ID.

        Args:
            kid: Key ID from JWT header

        Returns:
            Key dictionary or None if not found
        """
        jwks = await self.fetch_jwks()
        for key in jwks.get("keys", []):
            if key.get("kid") == kid:
                return key
        logger.warning(f"Key ID '{kid}' not found in JWKS")
        return None

    def clear_cache(self) -> None:
        """Clear JWKS cache (e.g., on key rotation)."""
        self.cached_jwks = None
        self.cache_time = None
        logger.info("JWKS cache cleared")

    def get_cache_status(self) -> Dict[str, Any]:
        """Get current cache status for monitoring."""
        return {
            "cached": self.cached_jwks is not None,
            "cache_time": self.cache_time.isoformat() if self.cache_time else None,
            "cache_valid": self._is_cache_valid(),
            "time_to_expiry": (
                (self.cache_time + self.cache_ttl - datetime.utcnow()).total_seconds()
                if self._is_cache_valid()
                else 0
            ),
            "has_fallback": self.last_known_good_jwks is not None,
            "in_backoff": self._is_backoff_active(),
            "backoff_attempts": self.backoff_attempts,
            "backoff_until": self.backoff_until.isoformat() if self.backoff_until else None,
        }
