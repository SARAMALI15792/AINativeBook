"""FastAPI dependencies for JWT authentication.

Provides:
- get_current_user: Extract and validate JWT from Authorization header
- require_role: Check user has required role(s)
- require_verified_email: Check email is verified
"""

import logging
from typing import Optional, List
from dataclasses import dataclass
from datetime import datetime

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials as HTTPAuthCredential
import jwt
from jwt import PyJWK, PyJWTError

from src.config.settings import get_settings
from src.core.auth.jwks import JWKSManager

logger = logging.getLogger(__name__)

# Security scheme for OpenAPI docs
security = HTTPBearer(auto_error=False)

# Global JWKS manager instance
_jwks_manager: Optional[JWKSManager] = None


def get_jwks_manager() -> JWKSManager:
    """Get or initialize JWKS manager."""
    global _jwks_manager
    if _jwks_manager is None:
        settings = get_settings()
        _jwks_manager = JWKSManager(
            jwks_url=settings.better_auth_jwks_url,
            cache_ttl_minutes=5,
        )
    return _jwks_manager


@dataclass
class AuthenticatedUser:
    """Authenticated user information from JWT claims."""

    id: str
    email: str
    name: Optional[str] = None
    email_verified: bool = False
    role: str = "student"  # Default role


async def get_current_user(
    credentials: Optional[HTTPAuthCredential] = Depends(security),
) -> AuthenticatedUser:
    """
    Extract and validate JWT token from Authorization header.

    Args:
        credentials: Bearer token from Authorization header

    Returns:
        AuthenticatedUser with claims

    Raises:
        HTTPException: 401 if token missing or invalid
    """
    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials
    settings = get_settings()

    try:
        # Get JWKS for verification
        jwks_manager = get_jwks_manager()
        jwks = await jwks_manager.fetch_jwks()

        # Decode JWT header to get kid (key ID)
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header.get("kid")

        if not kid:
            logger.warning("JWT missing 'kid' in header")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing key ID",
            )

        # Find the key in JWKS
        key_data = None
        for key in jwks.get("keys", []):
            if key.get("kid") == kid:
                key_data = key
                break

        if not key_data:
            logger.warning(f"Key ID '{kid}' not found in JWKS")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: key not found",
            )

        # Build a PyJWK from the key data to handle all key types
        # (RSA, EC, OKP/Ed25519) automatically
        jwk = PyJWK.from_dict(key_data)
        algorithm = jwk.algorithm_name  # e.g. "RS256", "EdDSA"

        # Verify JWT signature using the key
        decode_options = {}
        # EdDSA tokens from Better-Auth may use issuer/audience differently
        aud = settings.better_auth_audience or None
        iss = settings.better_auth_issuer or None

        payload = jwt.decode(
            token,
            jwk.key,
            algorithms=[algorithm],
            audience=aud,
            issuer=iss,
            options={
                "verify_aud": aud is not None,
                "verify_iss": iss is not None,
            },
        )

        # Extract user claims
        user_id = payload.get("sub") or payload.get("user_id")
        email = payload.get("email")

        if not user_id or not email:
            logger.warning(f"JWT missing required claims: sub={user_id}, email={email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing required claims",
            )

        # Create authenticated user object
        user = AuthenticatedUser(
            id=user_id,
            email=email,
            name=payload.get("name"),
            email_verified=payload.get("email_verified", False),
            role=payload.get("role", "student"),
        )

        logger.debug(f"✅ JWT validated for user {user.email} (role={user.role})")
        return user

    except PyJWTError as e:
        logger.warning(f"JWT validation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    except ValueError as e:
        logger.warning(f"JWKS fetch failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication service temporarily unavailable",
            headers={"Retry-After": "30"},
        )

    except Exception as e:
        logger.error(f"Unexpected error validating JWT: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication service error",
        )


async def require_role(
    *allowed_roles: str,
) -> callable:
    """
    Dependency factory for role-based access control.

    Usage:
        @app.get("/admin")
        async def admin_endpoint(user: AuthenticatedUser = Depends(require_role("admin"))):
            ...

    Args:
        allowed_roles: One or more allowed role names

    Returns:
        Dependency function that checks user has one of the roles
    """

    async def role_check(
        user: AuthenticatedUser = Depends(get_current_user),
    ) -> AuthenticatedUser:
        if user.role not in allowed_roles:
            logger.warning(
                f"Access denied: user {user.email} has role '{user.role}', "
                f"required one of {allowed_roles}"
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"This action requires one of these roles: {', '.join(allowed_roles)}",
            )
        return user

    return role_check


async def require_verified_email(
    user: AuthenticatedUser = Depends(get_current_user),
) -> AuthenticatedUser:
    """
    Require that user's email is verified.

    Raises:
        HTTPException: 403 if email not verified
    """
    if not user.email_verified:
        logger.warning(f"Access denied: user {user.email} email not verified")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email verification required. Check your inbox for verification link.",
        )
    return user


async def optional_user(
    credentials: Optional[HTTPAuthCredential] = Depends(security),
) -> Optional[AuthenticatedUser]:
    """
    Optional authentication - returns user if valid token present, None otherwise.

    Does not raise HTTPException like get_current_user.
    """
    if not credentials:
        return None

    try:
        user = await get_current_user(credentials)
        return user
    except HTTPException:
        return None


# Alias for backward compatibility
get_current_active_user = get_current_user


# Alias for backward compatibility
get_current_active_user = get_current_user
