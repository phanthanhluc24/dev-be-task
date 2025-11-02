from sqlalchemy.orm import Session
from sqlalchemy import exists, func
from sqlalchemy.exc import IntegrityError

from app.repositories.base import BaseRepository
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserUpdate


class UserRepository(BaseRepository):
    model = User

    def create_user(self, db: Session, data: UserCreate) -> User:
        new_user = User(name=data.name, email=data.email)

        db.add(new_user)
        self.commit_or_rollback(db)

        db.refresh(new_user)
        return new_user

    def get_by_id(self, db: Session, uid: int) -> User | None:
        return db.query(User).filter(User.id == uid).first()

    def get_by_email(self, db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()

    def list_users(self, db: Session, limit: int = 10, offset: int = 0):
        total = db.query(func.count(User.id)).scalar() or 0

        users = (
            db.query(User)
            .filter(User.is_delete.is_(None))
            .order_by(User.created_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

        return users, total

    def email_exists(self, db: Session, email: str) -> bool:
        return self.get_by_email(db, email) is not None

    def email_exists_exclude_id(
        self, db: Session, email: str, exclude_id: int | None = None
    ) -> bool:
        query = db.query(exists().where(User.email == email))

        if exclude_id is not None:
            query = query.filter(User.id != exclude_id)

        return db.scalar(query)


# Singleton instance
user_repository = UserRepository()
