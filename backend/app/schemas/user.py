"""User schemas for request/response validation."""

from datetime import datetime, date
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, ConfigDict


# Base schemas
class UserBase(BaseModel):
    """Base user schema."""

    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=255)


class UserProfileBase(BaseModel):
    """Base user profile schema."""

    date_of_birth: Optional[date] = None
    phone_number: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = None
    emergency_contact_name: Optional[str] = Field(None, max_length=255)
    emergency_contact_phone: Optional[str] = Field(None, max_length=20)
    medical_conditions: Optional[str] = None
    medications: Optional[str] = None
    allergies: Optional[str] = None
    preferences: dict = Field(default_factory=dict)


# Request schemas
class UserRegister(UserBase):
    """Schema for user registration."""

    password: str = Field(..., min_length=8, max_length=100)


class UserLogin(BaseModel):
    """Schema for user login."""

    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    """Schema for updating user information."""

    full_name: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[EmailStr] = None


class UserProfileUpdate(UserProfileBase):
    """Schema for updating user profile."""

    pass


# Response schemas
class UserResponse(UserBase):
    """Schema for user response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    role: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    last_login_at: Optional[datetime] = None


class UserProfileResponse(UserProfileBase):
    """Schema for user profile response."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime


class UserWithProfile(UserResponse):
    """Schema for user with profile."""

    profile: Optional[UserProfileResponse] = None


# Token schemas
class Token(BaseModel):
    """Schema for authentication token."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """Schema for token payload."""

    sub: UUID
    exp: datetime
    type: str  # 'access' or 'refresh'


class RefreshTokenRequest(BaseModel):
    """Schema for refresh token request."""

    refresh_token: str
