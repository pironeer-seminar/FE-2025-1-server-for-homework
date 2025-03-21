from typing import List
from sqlalchemy.orm import Session
from sqlmodel import select
from app.apps.user.model import User

class UserRepository:
    def __init__(self, db: Session):
        self._db = db
        print(type(db))

    def get_by_email(self, email: str):
        return self._db.query(User).filter(User.email == email).first()

    def create_user(self, user: User):
        self._db.add(user)
        self._db.commit()
        self._db.refresh(user)
        return user

    def get_users(self) -> List[User]:
        return self._db.execute(select(User)).scalars().all()
