from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.config.database import get_db

from app.schemas.user_schema import (
    UserCreate,
    UserListResponse,
    UserResponse,
    UserUpdate,
)
from app.services.user_service import user_service
from app.utils.response import response_created, response_success

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Create User",
)
async def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    user = user_service.create_user(db, user_data)
    return response_created(user)


@router.get("", summary="List Users")
async def list_users(
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    users = user_service.list_users(db, limit, offset)
    return response_success(users)


@router.get("/{user_id}", summary="Get User")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = user_service.get_user(db, user_id)
    return response_success(user)


@router.put("/{user_id}")
async def update_user_by_id(
    user_id: int, data: UserUpdate, db: Session = Depends(get_db)
):
    user = user_service.update_user_by_id(db, user_id, data)
    return response_success(user)


@router.delete("/{user_id}")
async def delete_user_by_id(user_id: int, db: Session = Depends(get_db)):
    res = user_service.delete_user_by_id(db, user_id)
    return response_success(message=res)
