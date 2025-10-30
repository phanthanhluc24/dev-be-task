"""
FastAPI application with user management endpoints.
"""

from contextlib import asynccontextmanager
from typing import List

from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .crud import user_crud
from .db import create_tables, get_db
from .schemas import (
    ErrorResponse,
    UserCreate,
    UserListResponse,
    UserResponse,
    ValidationErrorResponse,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    
    Creates database tables on startup and handles cleanup on shutdown.
    """
    # Startup: Create database tables
    create_tables()
    yield
    # Shutdown: Any cleanup code would go here


# Create FastAPI application
app = FastAPI(
    title="Users API",
    description="A simple REST API for managing users with FastAPI and SQLAlchemy",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)


@app.get(
    "/",
    summary="Health Check",
    description="Simple health check endpoint to verify the API is running",
    tags=["Health"]
)
async def root():
    """Root endpoint for health checks."""
    return {
        "message": "Users API is running!",
        "version": "0.1.0",
        "docs": "/docs"
    }


@app.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create User",
    description="Create a new user with name and email. Email must be unique.",
    responses={
        201: {
            "description": "User created successfully",
            "model": UserResponse,
        },
        400: {
            "description": "Email already exists or validation error",
            "model": ErrorResponse,
        },
        422: {
            "description": "Request validation error",
            "model": ValidationErrorResponse,
        },
    },
    tags=["Users"]
)
async def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
) -> UserResponse:
    """
    Create a new user.
    
    Args:
        user_data: User creation data (name and email)
        db: Database session dependency
        
    Returns:
        Created user with ID and timestamps
        
    Raises:
        HTTPException: 400 if email already exists
    """
    try:
        user = user_crud.create_user(db=db, user_data=user_data)
        return UserResponse.model_validate(user)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email '{user_data.email}' already exists"
        )


@app.get(
    "/users",
    response_model=UserListResponse,
    summary="List Users",
    description="Get a paginated list of all users",
    responses={
        200: {
            "description": "List of users retrieved successfully",
            "model": UserListResponse,
        },
        422: {
            "description": "Invalid query parameters",
            "model": ValidationErrorResponse,
        },
    },
    tags=["Users"]
)
async def list_users(
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
        description="Number of users to return (1-100)"
    ),
    offset: int = Query(
        default=0,
        ge=0,
        description="Number of users to skip"
    ),
    db: Session = Depends(get_db)
) -> UserListResponse:
    """
    Get a paginated list of users.
    
    Args:
        limit: Number of users to return (1-100)
        offset: Number of users to skip (0+)
        db: Database session dependency
        
    Returns:
        Paginated list of users with metadata
    """
    users, total = user_crud.get_users(db=db, limit=limit, offset=offset)
    
    return UserListResponse(
        users=[UserResponse.model_validate(user) for user in users],
        total=total,
        limit=limit,
        offset=offset
    )


@app.get(
    "/users/{user_id}",
    response_model=UserResponse,
    summary="Get User",
    description="Get a specific user by their ID",
    responses={
        200: {
            "description": "User retrieved successfully",
            "model": UserResponse,
        },
        404: {
            "description": "User not found",
            "model": ErrorResponse,
        },
    },
    tags=["Users"]
)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db)
) -> UserResponse:
    """
    Get a user by their ID.
    
    Args:
        user_id: User's unique identifier
        db: Database session dependency
        
    Returns:
        User details
        
    Raises:
        HTTPException: 404 if user not found
    """
    user = user_crud.get_user_by_id(db=db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    
    return UserResponse.model_validate(user)


# Custom exception handlers could be added here if needed
# For example, to handle specific database errors or validation errors
