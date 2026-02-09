"""
Authentication API routes.
"""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import service
from src.core.auth.models import User
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

router = APIRouter(prefix="/auth", tags=["authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_session)],
) -> User:
    """
    Dependency to get current authenticated user from token.

    Args:
        token: JWT access token from Authorization header
        db: Database session

    Returns:
        User: Current authenticated user

    Raises:
        HTTPException: If authentication fails
    """
    try:
        return await service.get_current_user(db, token)
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
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

    Args:
        user_data: User registration information
        db: Database session

    Returns:
        UserResponse: Created user information

    Raises:
        HTTPException: If email already exists
    """
    return await service.register_user(db, user_data)


@router.post("/login", response_model=SessionResponse)
async def login(
    credentials: UserLogin,
    request: Request,
    db: Annotated[AsyncSession, Depends(get_session)],
):
    """
    Login with email and password to receive access token.

    Args:
        credentials: User login credentials
        request: FastAPI request object (for IP and user agent)
        db: Database session

    Returns:
        SessionResponse: User information and access token

    Raises:
        HTTPException: If credentials are invalid
    """
    try:
        user, token = await service.login_user(db, credentials)

        # TODO: Store IP and user agent in session
        # (requires updating service.login_user to accept these)

        return SessionResponse(user=user, token=token)
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/token", response_model=Token)
async def token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[AsyncSession, Depends(get_session)],
):
    """
    OAuth2 compatible token endpoint for Swagger UI.

    Args:
        form_data: OAuth2 password flow form data
        db: Database session

    Returns:
        Token: Access token

    Raises:
        HTTPException: If credentials are invalid
    """
    try:
        credentials = UserLogin(email=form_data.username, password=form_data.password)
        _, token = await service.login_user(db, credentials)
        return token
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_session)],
):
    """
    Logout by invalidating current session.

    Args:
        token: Current access token
        db: Database session
    """
    await service.logout_user(db, token)


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
    # TODO: Check if current_user has admin role
    # For now, allowing any authenticated user (will be fixed with RBAC middleware)

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
    # TODO: Check if current_user has admin role

    await service.revoke_role(db, assignment.user_id, assignment.role_name)
