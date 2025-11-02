from typing import Any, Dict
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError


class BaseRepository:
    """Base repository cung cấp helper chung cho mọi repository."""

    @staticmethod
    def commit_or_rollback(db: Session):
        """
        Commit thay vì phải try/except trong từng repo.
        """
        try:
            db.commit()
        except SQLAlchemyError:
            db.rollback()
            raise

    def update_by_id(self, db: Session, obj_id: int, data: Dict[str, Any]):
        """
        Update object by id — repo không lo object có tồn tại hay không.
        Service sẽ kiểm tra trước khi gọi method này.
        """
        db_obj = db.query(self.model).filter(self.model.id == obj_id).first()

        # Không quan tâm None, service phải xử lý trước
        if not db_obj:
            return None

        # Cập nhật field
        for key, value in data.items():
            if hasattr(db_obj, key):
                setattr(db_obj, key, value)

        # Commit
        self.commit_or_rollback(db)

        # Refresh
        db.refresh(db_obj)
        return db_obj
