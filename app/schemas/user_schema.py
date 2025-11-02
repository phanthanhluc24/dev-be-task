"""
Pydantic schemas for request and response validation.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    """Base user schema with common fields."""

    name: str = Field(..., min_length=1, max_length=100, description="User's full name")
    email: EmailStr = Field(..., description="User's email address")


class UserCreate(UserBase):
    """Schema for creating a new user."""

    pass


class UserUpdate(UserBase):
    pass


class UserResponse(UserBase):
    """Schema for user response data."""

    id: int = Field(..., description="Unique user identifier")
    created_at: datetime = Field(..., description="User creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")

    model_config = ConfigDict(from_attributes=True)


class UserListResponse(BaseModel):
    """Schema for paginated user list response."""

    users: List[UserResponse] = Field(..., description="List of users")
    total: int = Field(..., description="Total number of users")
    limit: int = Field(..., description="Number of users per page")
    offset: int = Field(..., description="Number of users skipped")

    model_config = ConfigDict(from_attributes=True)


class ErrorResponse(BaseModel):
    """Schema for error responses."""

    detail: str = Field(..., description="Error message")
    error_code: Optional[str] = Field(
        None, description="Error code for programmatic handling"
    )


class ValidationErrorResponse(BaseModel):
    """Schema for validation error responses."""

    detail: List[dict] = Field(..., description="List of validation errors")
    error_code: str = Field(default="validation_error", description="Error code")


# Example request/response schemas for documentation
class ExampleUserCreate(BaseModel):
    """Example request body for creating a user."""

    name: str = "John Doe"
    email: str = "john.doe@example.com"


class ExampleUserResponse(BaseModel):
    """Example response for user creation."""

    id: int = 1
    name: str = "John Doe"
    email: str = "john.doe@example.com"
    created_at: datetime = datetime(2024, 1, 1, 12, 0, 0)
    updated_at: Optional[datetime] = None
