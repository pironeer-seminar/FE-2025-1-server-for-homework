from typing import List

from app.apps.user.repository import UserRepository
from app.apps.user.model import User
from sqlalchemy.orm import Session

class UserService:
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    def get_all_users(self) -> List[User]:
        return self._user_repository.get_users()

    def get_user(self, user_id) -> User:
        return self._user_repository.get_user_by_id(user_id)