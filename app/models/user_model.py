"""
SQLAlchemy database models.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.config.database import Base


class User(Base):
    """
    User model representing a user in the system.

    Attributes:
        id: Primary key, auto-incrementing integer
        name: User's full name
        email: User's email address (must be unique)
        created_at: Timestamp when the user was created
        updated_at: Timestamp when the user was last updated
    """

    __tablename__ = "users"

    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # User fields
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )

    is_delete: Mapped[bool] = mapped_column(Boolean, nullable=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )

    def __repr__(self) -> str:
        """String representation of User object."""
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}')>"
