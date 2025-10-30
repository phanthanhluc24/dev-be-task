"""
CRUD (Create, Read, Update, Delete) operations for users.
"""

from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .models import User
from .schemas import UserCreate


class UserCRUD:
    """Class containing CRUD operations for User model."""
    
    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        """
        Create a new user in the database.
        
        Args:
            db: Database session
            user_data: User data from request
            
        Returns:
            Created user object
            
        Raises:
            IntegrityError: If email already exists
        """
        db_user = User(
            name=user_data.name,
            email=user_data.email
        )
        
        try:
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return db_user
        except IntegrityError:
            db.rollback()
            raise
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """
        Get a user by their ID.
        
        Args:
            db: Database session
            user_id: User's unique identifier
            
        Returns:
            User object if found, None otherwise
        """
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """
        Get a user by their email address.
        
        Args:
            db: Database session
            email: User's email address
            
        Returns:
            User object if found, None otherwise
        """
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_users(
        db: Session, 
        limit: int = 10, 
        offset: int = 0
    ) -> tuple[List[User], int]:
        """
        Get a paginated list of users.
        
        Args:
            db: Database session
            limit: Maximum number of users to return
            offset: Number of users to skip
            
        Returns:
            Tuple of (list of users, total count)
        """
        # Get total count
        total = db.query(func.count(User.id)).scalar()
        
        # Get paginated users
        users = (
            db.query(User)
            .order_by(User.created_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )
        
        return users, total or 0
    
    @staticmethod
    def email_exists(db: Session, email: str) -> bool:
        """
        Check if an email already exists in the database.
        
        Args:
            db: Database session
            email: Email to check
            
        Returns:
            True if email exists, False otherwise
        """
        return db.query(User).filter(User.email == email).first() is not None


# Create a singleton instance for easy importing
user_crud = UserCRUD()
