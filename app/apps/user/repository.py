from typing import List
from sqlalchemy.orm import Session
from sqlmodel import select
from app.apps.user.model import User

class UserRepository:
    def __init__(self, db: Session):
        self._db = db
        print(type(db))

    def get_users(self) -> List[User]:
        return self._db.execute(select(User)).all()

    def get_user_by_id(self, user_id: int) -> User:
        return self._db.get(User, user_id)