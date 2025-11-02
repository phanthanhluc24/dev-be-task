from sqlalchemy.orm import Session
from app.exceptions.base import ConflictException, NotFoundException
from app.repositories.user_repository import user_repository
from app.schemas.user_schema import (
    UserCreate,
    UserListResponse,
    UserResponse,
    UserUpdate,
)


class UserService:
    def create_user(self, db: Session, data: UserCreate):
        if user_repository.email_exists(db, data.email):
            raise ConflictException("Email already exists")

        return user_repository.create_user(db, data)

    def get_user(self, db: Session, uid: int):
        user = user_repository.get_by_id(db, uid)
        if user is None:
            raise NotFoundException(message="User is not found")
        return user

    def get_user_by_email(self, db: Session, email: str):
        return user_repository.get_by_email(db, email)

    def list_users(self, db: Session, limit: int = 10, offset: int = 0):
        users, total = user_repository.list_users(db, limit, offset)

        return UserListResponse(
            users=[UserResponse.model_validate(u) for u in users],
            total=total,
            limit=limit,
            offset=offset,
        )

    def update_user_by_id(self, db: Session, uid: int, data: UserUpdate):
        is_user = user_repository.get_by_id(db, uid)
        if is_user is None:
            raise NotFoundException(message="User is not found")

        if data.email and data.email != is_user.email:
            if user_repository.email_exists_exclude_id(db, data.email, uid):
                raise ConflictException("Email already exists")

        return user_repository.update_by_id(db, uid, data.model_dump())

    def delete_user_by_id(self, db: Session, uid: int) -> str:
        is_user = user_repository.get_by_id(db, uid)
        if is_user is None:
            raise NotFoundException(message="User is not found")

        data = {"is_delete": True}

        user_repository.update_by_id(db, uid, data)

        return "Deleted user successfully"


# Singleton service
user_service = UserService()
