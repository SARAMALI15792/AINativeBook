"""
Authentication service with Better Auth integration for IntelliStack platform
"""
from datetime import datetime, timedelta, timezone
from typing import Optional, List, Dict, Any
import secrets

from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.config.settings import get_settings
from src.core.auth.models import User, Role, UserRole, Session, PasswordResetToken, LoginAttempt
from src.core.auth.schemas import (
    UserRegister,
    UserLogin,
    Token,
    TokenData,
    UserResponse,
)
from src.shared.exceptions import AuthenticationError, AuthorizationError, ConflictError, NotFoundError

settings = get_settings()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generate password hash"""
    return pwd_context.hash(password)


async def register_user(
    db: AsyncSession,
    user_data: UserRegister,
) -> UserResponse:
    """
    Register a new user with hashed password.
    This function will be used alongside Better Auth for initial user creation.

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
        raise ConflictError(
            resource="User",
            field="email",
            message="Email already registered",
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


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    """
    Retrieve a user by their email address.
    Used for Better Auth adapter integration.
    """
    result = await db.execute(
        select(User).where(User.email == email, User.deleted_at.is_(None))
    )
    return result.scalar_one_or_none()


async def get_user_by_id(db: AsyncSession, user_id: str) -> Optional[User]:
    """
    Retrieve a user by their ID.
    Used for Better Auth adapter integration.
    """
    result = await db.execute(
        select(User)
        .options(selectinload(User.roles))
        .where(User.id == user_id, User.deleted_at.is_(None))
    )
    return result.scalar_one_or_none()


async def get_user_roles(db: AsyncSession, user_id: str) -> List[str]:
    """
    Get roles assigned to a user.
    Used for authorization checks.
    """
    result = await db.execute(
        select(Role.name)
        .join(UserRole)
        .where(UserRole.user_id == user_id, UserRole.revoked_at.is_(None))
    )
    return [row[0] for row in result.all()]


async def get_current_user_from_token(
    db: AsyncSession,
    token_data: Dict[str, Any],
) -> User:
    """
    Get current user from Better Auth token data.

    Args:
        db: Database session
        token_data: Token data from Better Auth

    Returns:
        User: Current authenticated user

    Raises:
        AuthenticationError: If user not found
    """
    user_id = token_data.get("userId") or token_data.get("sub")
    if not user_id:
        raise AuthenticationError("Invalid token data")

    result = await db.execute(
        select(User)
        .options(selectinload(User.roles))
        .where(User.id == user_id, User.deleted_at.is_(None))
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
        raise NotFoundError(resource="User", resource_id=str(user_id))

    # Check role exists
    role_result = await db.execute(
        select(Role).where(Role.name == role_name)
    )
    role = role_result.scalar_one_or_none()
    if not role:
        raise NotFoundError(resource="Role", resource_id=role_name)

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
        raise ConflictError(
            resource="UserRole",
            message="Role already assigned to this user",
        )

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
        raise NotFoundError(resource="Role", resource_id=role_name)

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
        raise NotFoundError(resource="Role assignment")

    # Revoke
    assignment.revoked_at = datetime.now(timezone.utc)
    await db.commit()


# =============================================================================
# Password Recovery Functions
# =============================================================================

async def create_password_reset_token(
    db: AsyncSession,
    email: str,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
) -> Optional[str]:
    """
    Create a password reset token for a user.

    Args:
        db: Database session
        email: User's email address
        ip_address: IP address of the request
        user_agent: User agent of the request

    Returns:
        str: The plain token (to be sent via email) or None if user not found
    """
    # Find user
    result = await db.execute(
        select(User).where(User.email == email, User.deleted_at.is_(None))
    )
    user = result.scalar_one_or_none()

    if not user:
        # Don't reveal if user exists or not
        return None

    # Generate secure token
    plain_token = secrets.token_urlsafe(32)
    token_hash = get_password_hash(plain_token)[:255]  # Hash it for storage

    # Create token record
    expires_at = datetime.now(timezone.utc) + timedelta(hours=24)
    reset_token = PasswordResetToken(
        user_id=user.id,
        token_hash=token_hash,
        expires_at=expires_at,
        ip_address=ip_address,
        user_agent=user_agent,
    )

    db.add(reset_token)
    await db.commit()

    return plain_token


async def validate_password_reset_token(
    db: AsyncSession,
    token: str,
) -> Optional[User]:
    """
    Validate a password reset token and return the associated user.

    Args:
        db: Database session
        token: The plain token from the URL

    Returns:
        User: The user if token is valid, None otherwise
    """
    # Hash the token to compare with stored hash
    token_hash = get_password_hash(token)[:255]

    result = await db.execute(
        select(PasswordResetToken)
        .where(
            PasswordResetToken.token_hash == token_hash,
            PasswordResetToken.used_at.is_(None),
            PasswordResetToken.expires_at > datetime.now(timezone.utc),
        )
        .order_by(PasswordResetToken.created_at.desc())
    )
    reset_token = result.scalar_one_or_none()

    if not reset_token:
        return None

    # Get user
    result = await db.execute(
        select(User).where(User.id == reset_token.user_id)
    )
    user = result.scalar_one_or_none()

    return user


async def reset_password(
    db: AsyncSession,
    token: str,
    new_password: str,
) -> bool:
    """
    Reset a user's password using a valid token.

    Args:
        db: Database session
        token: The plain reset token
        new_password: The new password to set

    Returns:
        bool: True if successful, False otherwise
    """
    # Validate token
    user = await validate_password_reset_token(db, token)
    if not user:
        return False

    # Hash the token to find the record
    token_hash = get_password_hash(token)[:255]

    result = await db.execute(
        select(PasswordResetToken)
        .where(
            PasswordResetToken.token_hash == token_hash,
            PasswordResetToken.used_at.is_(None),
        )
        .order_by(PasswordResetToken.created_at.desc())
    )
    reset_token = result.scalar_one_or_none()

    if not reset_token:
        return False

    # Update password
    user.password_hash = get_password_hash(new_password)

    # Mark token as used
    reset_token.used_at = datetime.now(timezone.utc)

    # Clear failed login attempts
    user.failed_login_attempts = 0
    user.locked_until = None

    await db.commit()
    return True


# =============================================================================
# Security Functions - Account Lockout & Login Tracking
# =============================================================================

MAX_FAILED_ATTEMPTS = 5
LOCKOUT_DURATION_MINUTES = 30


async def record_login_attempt(
    db: AsyncSession,
    email: str,
    ip_address: str,
    was_successful: bool,
    user_agent: Optional[str] = None,
    failure_reason: Optional[str] = None,
) -> None:
    """
    Record a login attempt for security monitoring.

    Args:
        db: Database session
        email: Email attempted
        ip_address: Client IP address
        was_successful: Whether the login was successful
        user_agent: Client user agent
        failure_reason: Reason for failure (if applicable)
    """
    attempt = LoginAttempt(
        email=email,
        ip_address=ip_address,
        user_agent=user_agent,
        was_successful=was_successful,
        failure_reason=failure_reason,
    )
    db.add(attempt)
    await db.commit()


async def is_account_locked(
    db: AsyncSession,
    email: str,
) -> tuple[bool, Optional[datetime]]:
    """
    Check if an account is locked due to failed login attempts.

    Args:
        db: Database session
        email: User's email

    Returns:
        tuple: (is_locked, locked_until)
    """
    result = await db.execute(
        select(User).where(User.email == email, User.deleted_at.is_(None))
    )
    user = result.scalar_one_or_none()

    if not user:
        return False, None

    # Check if account is locked
    if user.locked_until and user.locked_until > datetime.now(timezone.utc):
        return True, user.locked_until

    # Check if lock has expired
    if user.locked_until and user.locked_until <= datetime.now(timezone.utc):
        # Clear the lock
        user.locked_until = None
        user.failed_login_attempts = 0
        await db.commit()
        return False, None

    return False, None


async def increment_failed_login(
    db: AsyncSession,
    email: str,
) -> None:
    """
    Increment failed login attempts for a user.
    Lock account if max attempts reached.

    Args:
        db: Database session
        email: User's email
    """
    result = await db.execute(
        select(User).where(User.email == email, User.deleted_at.is_(None))
    )
    user = result.scalar_one_or_none()

    if not user:
        return

    user.failed_login_attempts += 1

    # Lock account if max attempts reached
    if user.failed_login_attempts >= MAX_FAILED_ATTEMPTS:
        user.locked_until = datetime.now(timezone.utc) + timedelta(minutes=LOCKOUT_DURATION_MINUTES)

    await db.commit()


async def record_successful_login(
    db: AsyncSession,
    user_id: str,
    ip_address: Optional[str] = None,
) -> None:
    """
    Record a successful login and reset failed attempts.

    Args:
        db: Database session
        user_id: User's ID
        ip_address: Client IP address
    """
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if user:
        user.failed_login_attempts = 0
        user.locked_until = None
        user.last_login_at = datetime.now(timezone.utc)
        user.last_login_ip = ip_address
        await db.commit()


# =============================================================================
# Password Strength Validation
# =============================================================================

def validate_password_strength(password: str) -> tuple[bool, List[str]]:
    """
    Validate password strength according to security requirements.

    Requirements:
    - Minimum 12 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one number
    - At least one special character

    Args:
        password: Password to validate

    Returns:
        tuple: (is_valid, list_of_errors)
    """
    errors = []

    if len(password) < 12:
        errors.append("Password must be at least 12 characters long")

    if not any(c.isupper() for c in password):
        errors.append("Password must contain at least one uppercase letter")

    if not any(c.islower() for c in password):
        errors.append("Password must contain at least one lowercase letter")

    if not any(c.isdigit() for c in password):
        errors.append("Password must contain at least one number")

    special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    if not any(c in special_chars for c in password):
        errors.append("Password must contain at least one special character (!@#$%^&*()_+-=[]{}|;:,.<>?)")

    return len(errors) == 0, errors