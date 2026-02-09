"""
Authentication schemas for request/response validation.
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field


class Token(BaseModel):
    """OAuth2 token response"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds


class TokenData(BaseModel):
    """Data extracted from JWT token"""
    user_id: str
    email: str
    roles: List[str] = []


class UserRegister(BaseModel):
    """User registration request"""
    email: EmailStr
    name: str = Field(..., min_length=2, max_length=100)
    password: str = Field(..., min_length=8, max_length=100)


class UserLogin(BaseModel):
    """User login request"""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """User response (without sensitive data)"""
    id: str
    email: str
    name: str
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    is_active: bool
    roles: List[str] = []
    created_at: datetime

    model_config = {"from_attributes": True}


class RoleAssignment(BaseModel):
    """Role assignment request"""
    user_id: str
    role_name: str


class SessionResponse(BaseModel):
    """User session information"""
    user: UserResponse
    token: Token
