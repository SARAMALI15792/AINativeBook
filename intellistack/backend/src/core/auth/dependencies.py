"""FastAPI dependencies for JWT authentication.

Provides:
- get_current_user: Extract and validate JWT from Authorization header or session token from cookie
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
import httpx

from src.config.settings import get_settings
from src.core.auth.jwks import JWKSManager
from src.shared.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

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


async def validate_session_token(session_token: str) -> Optional[AuthenticatedUser]:
    """
    Validate a Better-Auth session token by calling the auth server.

    Args:
        session_token: The session token from the cookie

    Returns:
        AuthenticatedUser if valid, None if invalid
    """
    settings = get_settings()
    auth_server_url = settings.better_auth_jwks_url.replace('/.well-known/jwks.json', '')

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{auth_server_url}/api/auth/get-session",
                cookies={settings.better_auth_session_cookie_name: session_token},
                timeout=5.0
            )

            if response.status_code == 200:
                data = response.json()
                if data and data.get('user'):
                    user = data['user']
                    return AuthenticatedUser(
                        id=user.get('id'),
                        email=user.get('email'),
                        name=user.get('name'),
                        email_verified=user.get('emailVerified', False),
                        role=user.get('role', 'student')
                    )
            return None
    except Exception as e:
        logger.error(f"Failed to validate session token: {e}")
        return None


async def sync_user_from_jwt(
    user_id: str,
    email: str,
    name: Optional[str],
    email_verified: bool,
    role: str,
    db: AsyncSession
) -> None:
    """
    Ensure user exists in backend database, syncing from JWT claims if needed.

    This prevents foreign key violations when saving preferences or other user data.
    Better-Auth manages users in its own tables, but backend needs a copy for relationships.

    Args:
        user_id: User ID from JWT
        email: Email from JWT
        name: Name from JWT
        email_verified: Email verification status
        role: User role
        db: Database session
    """
    from src.core.auth.models import User

    try:
        # Check if user exists
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()

        if not user:
            # Create user in backend database
            user = User(
                id=user_id,
                email=email,
                name=name or email.split('@')[0],  # Fallback to email prefix
                password_hash='',  # Empty - managed by Better-Auth
                email_verified=email_verified,
                role=role,
                is_active=True,
                onboarding_completed=False,
                current_stage=1,
            )
            db.add(user)
            await db.commit()
            logger.info(f"✅ Synced user {email} (id={user_id}) to backend database")
        else:
            # Update user info if changed
            updated = False
            if user.email != email:
                user.email = email
                updated = True
            if user.name != name and name:
                user.name = name
                updated = True
            if user.email_verified != email_verified:
                user.email_verified = email_verified
                updated = True
            if user.role != role:
                user.role = role
                updated = True

            if updated:
                await db.commit()
                logger.debug(f"Updated user {email} info in backend database")

    except Exception as e:
        logger.error(f"Failed to sync user {email}: {e}")
        await db.rollback()
        # Don't raise - allow request to continue even if sync fails


async def get_current_user(
    request: Request,
    credentials: Optional[HTTPAuthCredential] = Depends(security),
    db: AsyncSession = Depends(get_session),
) -> AuthenticatedUser:
    """
    Extract and validate JWT token from Authorization header or session token from cookie.

    Args:
        request: FastAPI request object
        credentials: Bearer token from Authorization header (optional)

    Returns:
        AuthenticatedUser with claims

    Raises:
        HTTPException: 401 if token missing or invalid
    """
    settings = get_settings()

    # First, check if middleware already validated the user
    if hasattr(request.state, 'user') and request.state.user:
        user_data = request.state.user
        user = AuthenticatedUser(
            id=user_data['id'],
            email=user_data['email'],
            name=user_data.get('name'),
            email_verified=user_data.get('email_verified', False),
            role=user_data.get('role', 'student'),
        )

        # Sync user to backend database
        await sync_user_from_jwt(
            user_id=user.id,
            email=user.email,
            name=user.name,
            email_verified=user.email_verified,
            role=user.role,
            db=db,
        )

        return user

    # If middleware didn't validate, do it here
    # Try Authorization header first (JWT)
    token = credentials.credentials if credentials else None

    # Fallback to cookie (could be JWT or session token)
    if not token:
        token = request.cookies.get(settings.better_auth_session_cookie_name)

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Try to decode as JWT first
    try:
        # Get JWKS for verification
        jwks_manager = get_jwks_manager()
        jwks = await jwks_manager.fetch_jwks()

        # Decode JWT header to get kid (key ID)
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header.get("kid")

        if not kid:
            # Not a JWT, try session token validation
            raise jwt.DecodeError("Not a JWT")

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
        jwk = PyJWK.from_dict(key_data)
        algorithm = jwk.algorithm_name

        # Verify JWT signature using the key
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

        # Sync user to backend database
        await sync_user_from_jwt(
            user_id=user.id,
            email=user.email,
            name=user.name,
            email_verified=user.email_verified,
            role=user.role,
            db=db,
        )

        logger.debug(f"✅ JWT validated for user {user.email} (role={user.role})")
        return user

    except (PyJWTError, jwt.DecodeError) as e:
        # JWT validation failed, try session token validation
        logger.debug(f"JWT validation failed ({e}), trying session token validation")

        user = await validate_session_token(token)
        if user:
            # Sync user to backend database
            await sync_user_from_jwt(
                user_id=user.id,
                email=user.email,
                name=user.name,
                email_verified=user.email_verified,
                role=user.role,
                db=db,
            )
            logger.debug(f"✅ Session token validated for user {user.email} (role={user.role})")
            return user

        # Both JWT and session token validation failed
        logger.warning(f"Authentication failed: {e}")
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
    request: Request,
    credentials: Optional[HTTPAuthCredential] = Depends(security),
    db: AsyncSession = Depends(get_session),
) -> Optional[AuthenticatedUser]:
    """Optional authentication - returns user if valid token present, None otherwise."""
    if not credentials and not request.cookies.get(get_settings().better_auth_session_cookie_name):
        return None
    try:
        return await get_current_user(request, credentials, db)
    except HTTPException:
        return None


# Alias for backward compatibility
get_current_active_user = get_current_user

