"""
Authentication API routes with BetterAuth-compatible integration.
"""
from datetime import datetime, timedelta, timezone
from typing import Annotated, Dict, Any, Optional
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.config.logging import get_logger
from src.config.settings import get_settings
from src.core.auth import service_v2 as service
from src.core.auth.adapter import SQLAlchemyAdapter
from src.core.auth.better_auth_config import better_auth
from src.core.auth.models import User, Session as SessionModel
from src.core.auth.schemas import (
    UserRegister,
    UserLogin,
    UserResponse,
    SessionResponse,
    Token,
    RoleAssignment,
)
from src.shared.database import get_session
from src.shared.exceptions import AuthenticationError

logger = get_logger(__name__)

router = APIRouter(prefix="/auth", tags=["authentication"])


async def get_current_user_from_better_auth(
    request: Request,
    db: Annotated[AsyncSession, Depends(get_session)],
) -> User:
    """
    Dependency to get current authenticated user from Better Auth session.

    Args:
        request: FastAPI request object
        db: Database session

    Returns:
        User: Current authenticated user

    Raises:
        HTTPException: If authentication fails
    """
    # Extract session info from Better Auth (this would come from the middleware)
    # In a real implementation, Better Auth would provide this via request.state
    session_data = getattr(request.state, 'session', None)
    
    if not session_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        return await service.get_current_user_from_token(db, session_data)
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user_from_better_auth)],
) -> User:
    """
    Dependency to ensure user is active.

    Args:
        current_user: Current authenticated user

    Returns:
        User: Active user

    Raises:
        HTTPException: If user is inactive
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user account",
        )
    return current_user


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserRegister,
    db: Annotated[AsyncSession, Depends(get_session)],
):
    """
    Register a new user account.
    NOTE: With Better Auth, registration typically happens through Better Auth endpoints.
    This endpoint is kept for compatibility with existing flows.

    Args:
        user_data: User registration information
        db: Database session

    Returns:
        UserResponse: Created user information

    Raises:
        HTTPException: If email already exists
    """
    return await service.register_user(db, user_data)


@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """
    Get current user information.

    Args:
        current_user: Current authenticated user

    Returns:
        UserResponse: Current user information
    """
    return UserResponse.model_validate(current_user)


@router.post("/roles/assign", status_code=status.HTTP_204_NO_CONTENT)
async def assign_role_to_user(
    assignment: RoleAssignment,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
):
    """
    Assign a role to a user (admin only).

    Args:
        assignment: Role assignment data
        current_user: Current authenticated user (must be admin)
        db: Database session

    Raises:
        HTTPException: If user lacks admin permissions
    """
    # Check if current_user has admin role
    user_roles = await service.get_user_roles(db, str(current_user.id))
    if "platform_admin" not in user_roles and "institution_admin" not in user_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to assign roles",
        )

    await service.assign_role(
        db,
        assignment.user_id,
        assignment.role_name,
        str(current_user.id),
    )


@router.post("/roles/revoke", status_code=status.HTTP_204_NO_CONTENT)
async def revoke_role_from_user(
    assignment: RoleAssignment,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[AsyncSession, Depends(get_session)],
):
    """
    Revoke a role from a user (admin only).

    Args:
        assignment: Role assignment data
        current_user: Current authenticated user (must be admin)
        db: Database session

    Raises:
        HTTPException: If user lacks admin permissions
    """
    # Check if current_user has admin role
    user_roles = await service.get_user_roles(db, str(current_user.id))
    if "platform_admin" not in user_roles and "institution_admin" not in user_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to revoke roles",
        )

    await service.revoke_role(db, assignment.user_id, assignment.role_name)


@router.post("/login")
async def login(
    credentials: UserLogin,
    response: Response,
    db: Annotated[AsyncSession, Depends(get_session)],
):
    """
    Login with email and password, setting session cookie.

    Args:
        credentials: Email and password
        response: FastAPI response object for setting cookies
        db: Database session

    Returns:
        User info and session details
    """
    # Authenticate user
    user = await service.get_user_by_email(db, credentials.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Verify password
    adapter = SQLAlchemyAdapter(db)
    is_valid = await adapter.verify_password(str(user.id), credentials.password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive",
        )

    # Get user roles
    roles = await service.get_user_roles(db, str(user.id))

    # Create session in database
    session_token = str(uuid4())
    expires_at = datetime.now(timezone.utc) + timedelta(days=7)

    db_session = SessionModel(
        id=str(uuid4()),
        user_id=str(user.id),
        token=session_token,
        expires_at=expires_at,
    )
    db.add(db_session)
    await db.commit()

    # Create JWT session cookie
    jwt_token = better_auth.create_session_token(
        user_id=str(user.id),
        session_id=session_token,
    )

    # Set session cookie
    response.set_cookie(
        key=better_auth.cookie_name,
        value=jwt_token,
        httponly=better_auth.cookie_http_only,
        secure=better_auth.cookie_secure,
        samesite=better_auth.cookie_same_site,
        max_age=better_auth.cookie_max_age_days * 24 * 60 * 60,
    )

    logger.info("User logged in", user_id=str(user.id), email=user.email)

    return {
        "user": {
            "id": str(user.id),
            "email": user.email,
            "name": user.name,
            "emailVerified": user.is_verified,
            "image": user.avatar_url,
        },
        "session": {
            "token": jwt_token,
            "expiresAt": expires_at.isoformat(),
        },
    }


@router.post("/logout")
async def logout(
    request: Request,
    response: Response,
    db: Annotated[AsyncSession, Depends(get_session)],
):
    """
    Logout and clear session cookie.

    Args:
        request: FastAPI request object
        response: FastAPI response object for clearing cookies
        db: Database session
    """
    session_data = getattr(request.state, 'session', None)

    if session_data:
        # Revoke session in database
        session_id = session_data.get('sessionId')
        if session_id:
            result = await db.execute(
                select(SessionModel).where(SessionModel.token == session_id)
            )
            db_session = result.scalar_one_or_none()
            if db_session:
                db_session.revoked_at = datetime.now(timezone.utc)
                await db.commit()

        logger.info("User logged out", user_id=session_data.get('userId'))

    # Clear session cookie
    response.delete_cookie(
        key=better_auth.cookie_name,
        httponly=better_auth.cookie_http_only,
        secure=better_auth.cookie_secure,
        samesite=better_auth.cookie_same_site,
    )

    return {"success": True}


@router.get("/session")
async def get_session(
    request: Request,
    db: Annotated[AsyncSession, Depends(get_session)],
):
    """
    Get current session information.

    Args:
        request: FastAPI request object
        db: Database session

    Returns:
        Current session data if authenticated
    """
    session_data = getattr(request.state, 'session', None)

    if not session_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No active session",
        )

    user_id = session_data.get('userId')
    user = await service.get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return {
        "session": {
            "userId": str(user.id),
            "email": user.email,
            "name": user.name,
            "roles": session_data.get('roles', []),
        }
    }


# OAuth endpoints
@router.get("/oauth/{provider}")
async def oauth_authorize(provider: str, request: Request):
    """
    Initiate OAuth flow with a provider.

    Args:
        provider: OAuth provider name (google, github)
        request: FastAPI request

    Returns:
        Redirect to OAuth provider
    """
    if provider not in better_auth.oauth_providers:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported OAuth provider: {provider}",
        )

    oauth_client = better_auth.get_oauth_client(provider)
    config = better_auth.oauth_providers[provider]

    # Generate state for CSRF protection
    import secrets
    state = secrets.token_urlsafe(32)

    # Build authorization URL
    authorize_url = oauth_client.create_authorization_url(
        config["authorize_url"],
        state=state,
    )[0]

    # Store state in session (or use cache)
    response = RedirectResponse(url=authorize_url)
    response.set_cookie(
        key=f"oauth_state_{provider}",
        value=state,
        httponly=True,
        secure=better_auth.cookie_secure,
        samesite="lax",
        max_age=600,  # 10 minutes
    )

    return response


@router.get("/callback/{provider}")
async def oauth_callback(
    provider: str,
    code: str,
    state: str,
    request: Request,
    response: Response,
    db: Annotated[AsyncSession, Depends(get_session)],
):
    """
    Handle OAuth callback from provider.

    Args:
        provider: OAuth provider name
        code: Authorization code from provider
        state: CSRF state token
        request: FastAPI request
        response: FastAPI response for setting cookies
        db: Database session

    Returns:
        Redirect to frontend with session
    """
    if provider not in better_auth.oauth_providers:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported OAuth provider: {provider}",
        )

    # Verify state for CSRF protection
    stored_state = request.cookies.get(f"oauth_state_{provider}")
    if not stored_state or stored_state != state:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid OAuth state",
        )

    config = better_auth.oauth_providers[provider]
    oauth_client = better_auth.get_oauth_client(provider)

    try:
        # Exchange code for token
        token = await oauth_client.fetch_token(
            config["token_url"],
            code=code,
            client_secret=config["client_secret"],
        )

        # Fetch user info
        resp = await oauth_client.get(config["userinfo_url"])
        user_info = resp.json()

        # Extract email and name based on provider
        if provider == "google":
            email = user_info.get("email")
            name = user_info.get("name")
            provider_account_id = user_info.get("id")
            picture = user_info.get("picture")
        elif provider == "github":
            email = user_info.get("email")
            name = user_info.get("name") or user_info.get("login")
            provider_account_id = str(user_info.get("id"))
            picture = user_info.get("avatar_url")
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported provider: {provider}",
            )

        if not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email not provided by OAuth provider",
            )

        # All database operations for OAuth flow must be atomic
        async with db.begin():
            adapter = SQLAlchemyAdapter(db)

            # Check if user exists via OAuth account
            existing_user = await adapter.get_user_by_oauth_account(
                provider, provider_account_id
            )

            if existing_user:
                user_id = existing_user["id"]
                # Update tokens
                await adapter.link_oauth_account(
                    user_id=user_id,
                    provider=provider,
                    provider_account_id=provider_account_id,
                    access_token=token.get("access_token"),
                    refresh_token=token.get("refresh_token"),
                    expires_at=datetime.now(timezone.utc) + timedelta(seconds=token.get("expires_in", 3600)) if token.get("expires_in") else None,
                    token_type=token.get("token_type"),
                    scope=token.get("scope"),
                )
            else:
                # Check if user exists with same email
                existing_user = await adapter.get_user_by_email(email)

                if existing_user:
                    # Link OAuth to existing account
                    user_id = existing_user["id"]
                    await adapter.link_oauth_account(
                        user_id=user_id,
                        provider=provider,
                        provider_account_id=provider_account_id,
                        access_token=token.get("access_token"),
                        refresh_token=token.get("refresh_token"),
                        expires_at=datetime.now(timezone.utc) + timedelta(seconds=token.get("expires_in", 3600)) if token.get("expires_in") else None,
                        token_type=token.get("token_type"),
                        scope=token.get("scope"),
                    )
                else:
                    # Create new user with OAuth account in a single transaction
                    import secrets
                    temp_password = secrets.token_urlsafe(32)
                    new_user = await adapter.create_user(
                        email=email,
                        password=temp_password,
                        name=name or email.split("@")[0],
                        email_verified=True,
                        avatar_url=picture,
                        commit=False,  # Don't commit yet - let transaction handle it
                    )
                    user_id = new_user["id"]

                    # Link OAuth account (part of same transaction)
                    await adapter.link_oauth_account(
                        user_id=user_id,
                        provider=provider,
                        provider_account_id=provider_account_id,
                        access_token=token.get("access_token"),
                        refresh_token=token.get("refresh_token"),
                        expires_at=datetime.now(timezone.utc) + timedelta(seconds=token.get("expires_in", 3600)) if token.get("expires_in") else None,
                        token_type=token.get("token_type"),
                        scope=token.get("scope"),
                        commit=False,  # Don't commit yet - let transaction handle it
                    )

        # Get user roles
        roles = await adapter.get_user_roles(user_id)

        # Create session
        session_token = str(uuid4())
        expires_at = datetime.now(timezone.utc) + timedelta(days=7)

        db_session = SessionModel(
            id=str(uuid4()),
            user_id=user_id,
            token=session_token,
            expires_at=expires_at,
        )
        db.add(db_session)
        await db.commit()

        # Create JWT session cookie
        jwt_token = better_auth.create_session_token(
            user_id=user_id,
            session_id=session_token,
        )

        # Set session cookie
        response.set_cookie(
            key=better_auth.cookie_name,
            value=jwt_token,
            httponly=better_auth.cookie_http_only,
            secure=better_auth.cookie_secure,
            samesite=better_auth.cookie_same_site,
            max_age=better_auth.cookie_max_age_days * 24 * 60 * 60,
        )

        # Clear OAuth state cookie
        response.delete_cookie(key=f"oauth_state_{provider}")

        logger.info("OAuth login successful", provider=provider, user_id=user_id)

        # Redirect to frontend using configurable settings
        settings = get_settings()
        redirect_url = f"{settings.frontend_url}{settings.post_login_redirect_path}"
        return RedirectResponse(url=redirect_url)

    except HTTPException:
        # Re-raise HTTP exceptions as-is (they have specific status codes)
        raise
    except Exception as e:
        import traceback
        error_details = {
            "error": str(e),
            "error_type": type(e).__name__,
            "provider": provider,
            "traceback": traceback.format_exc(),
        }
        logger.error("OAuth callback failed with exception", **error_details)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"OAuth authentication failed: {type(e).__name__}",
        )


# =============================================================================
# Password Reset Endpoints
# =============================================================================

class ForgotPasswordRequest(BaseModel):
    """Request body for forgot password."""
    email: str


class ResetPasswordRequest(BaseModel):
    """Request body for password reset."""
    token: str
    new_password: str


@router.post("/forgot-password", status_code=status.HTTP_200_OK)
async def forgot_password(
    request_data: ForgotPasswordRequest,
    request: Request,
    db: Annotated[AsyncSession, Depends(get_session)],
):
    """
    Request a password reset email.

    Args:
        request_data: Contains the email address
        request: FastAPI request object for IP/user agent
        db: Database session

    Returns:
        Success message (always returns 200 to prevent email enumeration)
    """
    client_ip = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")

    # Create password reset token (returns None if user not found)
    token = await service.create_password_reset_token(
        db,
        email=request_data.email,
        ip_address=client_ip,
        user_agent=user_agent,
    )

    if token:
        # TODO: Send email with reset link
        # For now, log the token for development purposes
        # In production, this would send an email
        logger.info(
            "Password reset requested",
            email=request_data.email,
            ip_address=client_ip,
            # In dev mode, include the token for testing
            token=token if not better_auth.cookie_secure else None,
        )

        # TODO: Integrate with email service
        # Example email content:
        # reset_url = f"{frontend_url}/reset-password?token={token}"
        # await email_service.send_password_reset(email, reset_url)

    # Always return success to prevent email enumeration attacks
    return {
        "message": "If an account exists with this email, you will receive password reset instructions shortly."
    }


@router.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(
    request_data: ResetPasswordRequest,
    db: Annotated[AsyncSession, Depends(get_session)],
):
    """
    Reset password using a valid reset token.

    Args:
        request_data: Contains the reset token and new password
        db: Database session

    Returns:
        Success message or error if token invalid

    Raises:
        HTTPException: If token is invalid or password doesn't meet requirements
    """
    # Validate password strength
    is_valid, errors = service.validate_password_strength(request_data.new_password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Password does not meet requirements", "errors": errors},
        )

    # Reset the password
    success = await service.reset_password(db, request_data.token, request_data.new_password)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token",
        )

    logger.info("Password reset successful")

    return {"message": "Password has been reset successfully. You can now log in with your new password."}


@router.get("/verify-reset-token")
async def verify_reset_token(
    token: str,
    db: Annotated[AsyncSession, Depends(get_session)],
):
    """
    Verify if a password reset token is valid.

    Args:
        token: The reset token from the URL
        db: Database session

    Returns:
        Valid status and user email if valid
    """
    user = await service.validate_password_reset_token(db, token)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token",
        )

    return {"valid": True, "email": user.email}