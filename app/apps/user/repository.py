from uuid import UUID
from typing import List
from sqlalchemy.orm import Session
from sqlmodel import select

from app.apps.user.model import User

class UserRepository:
    def __init__(self, db: Session):
        self._db = db
    def get_user_by_email(self, email: str):
        return self._db.query(User).filter(User.email == email).first()

    def get_user_by_id(self, user_id: UUID):
        return self._db.query(User).filter(User.id == user_id).first()

    def create_user(self, user: User):
        self._db.add(user)
        self._db.commit()
        self._db.refresh(user)
        return user

    def put_user(self, user_id: UUID, user: User):
        updated_user = self.get_user_by_id(user_id)
        if user.name is not None:
            updated_user.name = user.name
        if user.slogan is not None:
            updated_user.slogan = user.slogan
        if user.favorites is not None:
            updated_user.favorites = user.favorites

        self._db.commit()
        self._db.refresh(updated_user)
        return updated_user