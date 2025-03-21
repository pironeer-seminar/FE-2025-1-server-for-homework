import os
import jwt
from uuid import UUID
from typing import List

from app.apps.common.enums import TokenType
from app.apps.user.repository import UserRepository
from app.apps.user.repository import User
from app.apps.middleware.exceptions import ExpiredSignatureError
from app.apps.middleware.exceptions import InvalidTokenError
from app.apps.middleware.exceptions import BlockedTokenError

class MiddlewareService:
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    def validate_access_token(self, token: str) -> str:
        try:
            payload = jwt.decode(
                token,
                os.getenv("JWT_SECRET_KEY"),
                algorithms=["HS256"],
                options={"require": ["sub"]},
            )
        except jwt.ExpiredSignatureError as exec:
            raise ExpiredSignatureError from exec
        except jwt.InvalidTokenError as exec:
            raise InvalidTokenError from exec
        
        if payload["typ"] != TokenType.ACCESS.value:
            raise InvalidTokenError

        return payload["sub"]

    def validate_refresh_token(self, token:str) -> str:
        try:
            payload = jwt.decode(
                token,
                os.getenv("JWT_SECRET_KEY"),
                algorithms=["HS256"],
                options={"require": ["sub"]},
            )
        except jwt.ExpiredSignatureError as exec:
            raise ExpiredSignatureError from exec
        except jwt.InvalidTokenError as exec:
            raise InvalidTokenError from exec

        if payload["typ"] != TokenType.REFRESH.value:
            raise InvalidTokenError

        if self._user_repository.is_token_blocked(payload["jti"]):
            raise BlockedTokenError

        return payload["sub"]

    def get_current_user(self, token: str) -> User:
        id = self.validate_access_token(token)

        try:
            uuid_id = UUID(id)
        except ValueError as exc:
            raise InvalidTokenError from exc
        
        user = self._user_repository.get_user_by_id(uuid_id)
        if user is None:
            raise InvalidTokenError
        return user
    
    def favoriteStringToList(self, favorites: str | None) -> List[str] | None:
        if favorites is None or favorites == "":
            return None
        if favorites == "":
            return favorites.split(',')
