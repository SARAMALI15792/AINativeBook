"""
Authentication service with JWT token generation and validation.
"""
from datetime import datetime, timedelta, timezone
from typing import Optional, List
import secrets

import jwt
from fastapi import HTTPException, status
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.config.settings import get_settings
from src.core.auth.models import User, Role, UserRole, Session
from src.core.auth.schemas import (
    UserRegister,
    UserLogin,
    Token,
    TokenData,
    UserResponse,
)
from src.shared.exceptions import AuthenticationError, AuthorizationError

settings = get_settings()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generate password hash"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc)})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> TokenData:
    """Decode and validate JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        email: str = payload.get("email")
        roles: List[str] = payload.get("roles", [])

        if user_id is None or email is None:
            raise AuthenticationError("Invalid token payload")

        return TokenData(user_id=user_id, email=email, roles=roles)
    except jwt.ExpiredSignatureError:
        raise AuthenticationError("Token has expired")
    except jwt.InvalidTokenError:
        raise AuthenticationError("Invalid token")


async def register_user(
    db: AsyncSession,
    user_data: UserRegister,
) -> UserResponse:
    """
    Register a new user with hashed password.

    Args:
        db: Database session
        user_data: User registration data

    Returns:
        UserResponse: Created user information

    Raises:
        HTTPException: If email already exists
    """
    # Check if user exists
    result = await db.execute(
        select(User).where(User.email == user_data.email, User.deleted_at.is_(None))
    )
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Create user
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        name=user_data.name,
        password_hash=hashed_password,
        is_active=True,
    )

    db.add(new_user)
    await db.flush()

    # Assign default 'student' role
    student_role_result = await db.execute(
        select(Role).where(Role.name == "student")
    )
    student_role = student_role_result.scalar_one_or_none()

    if student_role:
        user_role = UserRole(
            user_id=new_user.id,
            role_id=student_role.id,
            granted_by=new_user.id,  # Self-assigned on registration
        )
        db.add(user_role)

    await db.commit()
    await db.refresh(new_user)

    # Load roles
    result = await db.execute(
        select(User)
        .options(selectinload(User.roles))
        .where(User.id == new_user.id)
    )
    user_with_roles = result.scalar_one()

    return UserResponse.model_validate(user_with_roles)


async def login_user(
    db: AsyncSession,
    credentials: UserLogin,
) -> tuple[UserResponse, Token]:
    """
    Authenticate user and generate access token.

    Args:
        db: Database session
        credentials: User login credentials

    Returns:
        tuple: (UserResponse, Token)

    Raises:
        AuthenticationError: If credentials are invalid
    """
    # Find user
    result = await db.execute(
        select(User)
        .options(selectinload(User.roles))
        .where(User.email == credentials.email, User.deleted_at.is_(None))
    )
    user = result.scalar_one_or_none()

    if not user or not verify_password(credentials.password, user.password_hash):
        raise AuthenticationError("Incorrect email or password")

    if not user.is_active:
        raise AuthenticationError("Account is inactive")

    # Get role names
    role_result = await db.execute(
        select(Role.name)
        .join(UserRole)
        .where(UserRole.user_id == user.id, UserRole.revoked_at.is_(None))
    )
    role_names = [row[0] for row in role_result.all()]

    # Create access token
    token_data = {
        "sub": str(user.id),
        "email": user.email,
        "roles": role_names,
    }
    access_token = create_access_token(token_data)

    # Create session record
    session = Session(
        user_id=user.id,
        token=access_token,
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        ip_address=None,  # Should be set by route handler
        user_agent=None,  # Should be set by route handler
    )
    db.add(session)
    await db.commit()

    token = Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )

    user_response = UserResponse.model_validate(user)
    user_response.roles = role_names

    return user_response, token


async def get_current_user(
    db: AsyncSession,
    token: str,
) -> User:
    """
    Get current user from JWT token.

    Args:
        db: Database session
        token: JWT access token

    Returns:
        User: Current authenticated user

    Raises:
        AuthenticationError: If token is invalid or user not found
    """
    token_data = decode_access_token(token)

    result = await db.execute(
        select(User)
        .options(selectinload(User.roles))
        .where(User.id == token_data.user_id, User.deleted_at.is_(None))
    )
    user = result.scalar_one_or_none()

    if user is None:
        raise AuthenticationError("User not found")

    if not user.is_active:
        raise AuthenticationError("User account is inactive")

    return user


async def assign_role(
    db: AsyncSession,
    user_id: str,
    role_name: str,
    granted_by_id: str,
) -> None:
    """
    Assign a role to a user.

    Args:
        db: Database session
        user_id: Target user ID
        role_name: Role name to assign
        granted_by_id: Admin user ID granting the role

    Raises:
        HTTPException: If user or role not found
    """
    # Check user exists
    user_result = await db.execute(
        select(User).where(User.id == user_id, User.deleted_at.is_(None))
    )
    user = user_result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check role exists
    role_result = await db.execute(
        select(Role).where(Role.name == role_name)
    )
    role = role_result.scalar_one_or_none()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    # Check if already assigned
    existing_result = await db.execute(
        select(UserRole).where(
            UserRole.user_id == user_id,
            UserRole.role_id == role.id,
            UserRole.revoked_at.is_(None),
        )
    )
    existing = existing_result.scalar_one_or_none()

    if existing:
        raise HTTPException(status_code=400, detail="Role already assigned")

    # Create assignment
    user_role = UserRole(
        user_id=user_id,
        role_id=role.id,
        granted_by=granted_by_id,
    )
    db.add(user_role)
    await db.commit()


async def revoke_role(
    db: AsyncSession,
    user_id: str,
    role_name: str,
) -> None:
    """
    Revoke a role from a user (soft delete).

    Args:
        db: Database session
        user_id: Target user ID
        role_name: Role name to revoke

    Raises:
        HTTPException: If role assignment not found
    """
    # Find role
    role_result = await db.execute(
        select(Role).where(Role.name == role_name)
    )
    role = role_result.scalar_one_or_none()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    # Find assignment
    assignment_result = await db.execute(
        select(UserRole).where(
            UserRole.user_id == user_id,
            UserRole.role_id == role.id,
            UserRole.revoked_at.is_(None),
        )
    )
    assignment = assignment_result.scalar_one_or_none()

    if not assignment:
        raise HTTPException(status_code=404, detail="Role assignment not found")

    # Revoke
    assignment.revoked_at = datetime.now(timezone.utc)
    await db.commit()


async def logout_user(
    db: AsyncSession,
    token: str,
) -> None:
    """
    Logout user by invalidating session.

    Args:
        db: Database session
        token: JWT access token to invalidate
    """
    # Find and invalidate session
    result = await db.execute(
        select(Session).where(Session.token == token, Session.revoked_at.is_(None))
    )
    session = result.scalar_one_or_none()

    if session:
        session.revoked_at = datetime.now(timezone.utc)
        await db.commit()
