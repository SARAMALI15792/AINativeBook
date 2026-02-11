"""
Database adapter for BetterAuth-compatible authentication with IntelliStack's SQLAlchemy models.

This adapter provides a translation layer between BetterAuth's expected user format and
IntelliStack's SQLAlchemy models. It handles user CRUD operations, session management,
and OAuth account linking.
"""
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload

from src.core.auth.models import User as DBUser, Role, UserRole, OAuthAccount
from src.core.auth.service import get_password_hash, verify_password


class SQLAlchemyAdapter:
    """
    SQLAlchemy adapter for BetterAuth-compatible authentication.

    Maps between BetterAuth's expected user format:
    {
        "id": str,
        "email": str,
        "emailVerified": bool,
        "name": str,
        "image": str (optional),
        "createdAt": str (ISO format),
        "updatedAt": str (ISO format),
    }

    And IntelliStack's SQLAlchemy User model with fields like:
    - id, email, name, password_hash, is_verified, avatar_url, bio, locale, is_active, etc.
    """

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    def _to_betterauth_format(self, user: DBUser) -> Dict[str, Any]:
        """Convert SQLAlchemy User to BetterAuth format."""
        return {
            "id": str(user.id),
            "email": user.email,
            "emailVerified": user.is_verified,
            "name": user.name,
            "image": user.avatar_url,
            "createdAt": user.created_at.isoformat() if user.created_at else None,
            "updatedAt": user.updated_at.isoformat() if user.updated_at else None,
        }

    async def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Retrieve a user by their email address in BetterAuth format."""
        result = await self.db_session.execute(
            select(DBUser).where(
                and_(DBUser.email == email, DBUser.deleted_at.is_(None))
            )
        )
        user = result.scalar_one_or_none()
        return self._to_betterauth_format(user) if user else None

    async def create_user(
        self, email: str, password: str, name: str, commit: bool = True, **kwargs
    ) -> Dict[str, Any]:
        """Create a new user in the database with default student role.

        Args:
            email: User's email address
            password: Plain text password (will be hashed)
            name: User's display name
            commit: Whether to commit the transaction (default True). Set to False
                   when this is part of a larger transaction.
            **kwargs: Additional user attributes (email_verified, avatar_url, bio, locale)

        Returns:
            Dict containing user data in BetterAuth format
        """
        hashed_password = get_password_hash(password)
        new_user = DBUser(
            email=email,
            name=name,
            password_hash=hashed_password,
            is_active=True,
            is_verified=kwargs.get("email_verified", False),
            avatar_url=kwargs.get("avatar_url"),
            bio=kwargs.get("bio"),
            locale=kwargs.get("locale", "en"),
        )
        self.db_session.add(new_user)
        await self.db_session.flush()  # Get the ID without committing

        # Assign default 'student' role
        student_role_result = await self.db_session.execute(
            select(Role).where(Role.name == "student")
        )
        student_role = student_role_result.scalar_one_or_none()

        if student_role:
            user_role = UserRole(
                user_id=new_user.id,
                role_id=student_role.id,
                granted_by=new_user.id,  # Self-assigned on registration
            )
            self.db_session.add(user_role)

        if commit:
            await self.db_session.commit()
            await self.db_session.refresh(new_user)

        return self._to_betterauth_format(new_user)

    async def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a user by their ID in BetterAuth format."""
        result = await self.db_session.execute(
            select(DBUser).where(
                and_(DBUser.id == user_id, DBUser.deleted_at.is_(None))
            )
        )
        user = result.scalar_one_or_none()
        return self._to_betterauth_format(user) if user else None

    async def update_password(self, user_id: str, new_password: str) -> bool:
        """Update a user's password."""
        result = await self.db_session.execute(
            select(DBUser).where(DBUser.id == user_id)
        )
        user = result.scalar_one()
        user.password_hash = get_password_hash(new_password)
        await self.db_session.commit()
        return True

    async def verify_password(self, user_id: str, password: str) -> bool:
        """Verify a user's password."""
        result = await self.db_session.execute(
            select(DBUser).where(DBUser.id == user_id)
        )
        user = result.scalar_one()
        return verify_password(password, user.password_hash)

    async def update_user(self, user_id: str, **kwargs) -> bool:
        """Update user information."""
        result = await self.db_session.execute(
            select(DBUser).where(DBUser.id == user_id)
        )
        user = result.scalar_one()

        # Update allowed fields with mapping from BetterAuth format
        field_mapping = {
            "name": "name",
            "email_verified": "is_verified",
            "emailVerified": "is_verified",
            "avatar_url": "avatar_url",
            "image": "avatar_url",
            "bio": "bio",
            "locale": "locale",
        }

        for key, value in kwargs.items():
            if key in field_mapping and value is not None:
                setattr(user, field_mapping[key], value)

        await self.db_session.commit()
        return True

    async def get_user_roles(self, user_id: str) -> List[str]:
        """Get roles assigned to a user."""
        result = await self.db_session.execute(
            select(Role.name)
            .join(UserRole)
            .where(
                and_(
                    UserRole.user_id == user_id,
                    UserRole.revoked_at.is_(None),
                )
            )
        )
        return [row[0] for row in result.all()]

    async def link_oauth_account(
        self,
        user_id: str,
        provider: str,
        provider_account_id: str,
        access_token: str,
        refresh_token: Optional[str] = None,
        expires_at: Optional[datetime] = None,
        token_type: Optional[str] = None,
        scope: Optional[str] = None,
        id_token: Optional[str] = None,
        commit: bool = True,
    ) -> bool:
        """Link an OAuth account to an existing user.

        Args:
            user_id: The user's ID
            provider: OAuth provider name (e.g., 'google', 'github')
            provider_account_id: Provider-specific account ID
            access_token: OAuth access token
            refresh_token: OAuth refresh token (optional)
            expires_at: Token expiration datetime (optional)
            token_type: Token type (e.g., 'Bearer') (optional)
            scope: OAuth scope (optional)
            id_token: OpenID Connect ID token (optional)
            commit: Whether to commit the transaction (default True). Set to False
                   when this is part of a larger transaction.

        Returns:
            True if successful
        """
        # Check if account already linked
        existing_result = await self.db_session.execute(
            select(OAuthAccount).where(
                and_(
                    OAuthAccount.user_id == user_id,
                    OAuthAccount.provider == provider,
                    OAuthAccount.provider_account_id == provider_account_id,
                )
            )
        )
        existing = existing_result.scalar_one_or_none()

        if existing:
            # Update existing account
            existing.access_token = access_token
            existing.refresh_token = refresh_token
            existing.expires_at = expires_at
            existing.token_type = token_type
            existing.scope = scope
            existing.id_token = id_token
            existing.updated_at = datetime.now(timezone.utc)
        else:
            # Create new OAuth account link
            oauth_account = OAuthAccount(
                id=str(uuid4()),
                user_id=user_id,
                provider=provider,
                provider_account_id=provider_account_id,
                access_token=access_token,
                refresh_token=refresh_token,
                expires_at=expires_at,
                token_type=token_type,
                scope=scope,
                id_token=id_token,
            )
            self.db_session.add(oauth_account)

        if commit:
            await self.db_session.commit()
        return True

    async def get_oauth_accounts(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all OAuth accounts linked to a user."""
        result = await self.db_session.execute(
            select(OAuthAccount).where(OAuthAccount.user_id == user_id)
        )
        accounts = result.scalars().all()

        return [
            {
                "id": str(acc.id),
                "provider": acc.provider,
                "providerAccountId": acc.provider_account_id,
                "createdAt": acc.created_at.isoformat() if acc.created_at else None,
            }
            for acc in accounts
        ]

    async def unlink_oauth_account(
        self, user_id: str, provider: str, provider_account_id: str
    ) -> bool:
        """Unlink an OAuth account from a user."""
        result = await self.db_session.execute(
            select(OAuthAccount).where(
                and_(
                    OAuthAccount.user_id == user_id,
                    OAuthAccount.provider == provider,
                    OAuthAccount.provider_account_id == provider_account_id,
                )
            )
        )
        account = result.scalar_one_or_none()

        if account:
            await self.db_session.delete(account)
            await self.db_session.commit()
            return True
        return False

    async def get_user_by_oauth_account(
        self, provider: str, provider_account_id: str
    ) -> Optional[Dict[str, Any]]:
        """Find a user by their OAuth account (for social login)."""
        result = await self.db_session.execute(
            select(OAuthAccount)
            .options(selectinload(OAuthAccount.user))
            .where(
                and_(
                    OAuthAccount.provider == provider,
                    OAuthAccount.provider_account_id == provider_account_id,
                )
            )
        )
        oauth_account = result.scalar_one_or_none()

        if oauth_account and oauth_account.user:
            return self._to_betterauth_format(oauth_account.user)
        return None
