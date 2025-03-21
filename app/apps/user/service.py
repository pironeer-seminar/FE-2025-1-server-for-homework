import os
import bcrypt
import jwt
from uuid import UUID
from datetime import datetime, timedelta
from typing import List
from sqlalchemy.exc import IntegrityError

from app.apps.common.enums import TokenType
from app.apps.middleware.service import MiddlewareService
from app.apps.user.repository import UserRepository
from app.apps.user.repository import User
from app.apps.user.schemas import SignUpRequest
from app.apps.user.schemas import SignInRequest
from app.apps.user.schemas import UserWithToken
from app.apps.user.schemas import UserResponse
from app.apps.user.schemas import PutNameRequest
from app.apps.user.schemas import PutSloganRequest
from app.apps.user.schemas import PutFavoritesRequest
from app.apps.user.exceptions import EmailAlreadyExistsException
from app.apps.user.exceptions import UserAlreadyExistsException
from app.apps.user.exceptions import UserNotFoundException
from app.apps.common.common_exception import InvalidFormException
from app.apps.common.common_exception import UserPermissionDeniedException

MAX_FAVORITES_SIZE = 10

class UserService:
    def __init__(self, user_repository: UserRepository, middleware: MiddlewareService):
        self._user_repository = user_repository
        self._middleware = middleware

    def _hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

    def _issue_token(self, id: UUID) -> tuple[str, str]:
        access_payload = {
            "sub": str(id),
            "exp": datetime.now() + timedelta(minutes=5),
            "typ": TokenType.ACCESS.value,
        }
        access_token = jwt.encode(access_payload, os.getenv("JWT_SECRET_KEY"), algorithm="HS256")

        return access_token

    def sign_up_user(self, request: SignUpRequest):
        if self._user_repository.get_user_by_email(request.email):
            raise EmailAlreadyExistsException

        hashed_password = self._hash_password(request.password)
        user_request = User(
            name=request.name,
            email=request.email,
            password=hashed_password,
        )

        try:
            user = self._user_repository.create_user(user_request)
            token = self._issue_token(user.id)
        except ValueError as exc:
            raise InvalidFormException from exc
        except IntegrityError as exc:
            raise UserAlreadyExistsException from exc

        return UserWithToken(id=user.id, name=user.name, email=user.email, token=token)

    def sign_in_user(self, request: SignInRequest):
        user = self._user_repository.get_user_by_email(request.email)
        if not user:
            raise UserNotFoundException
        if not self._verify_password(request.password, user.password):
            raise UserPermissionDeniedException

        token = self._issue_token(user.id)
        return UserWithToken(id=user.id, name=user.name, email=user.email, token=token)

    def get_my_info(self, token: str):
        user=self._middleware.get_current_user(token)
        if not user:
            raise UserNotFoundException
        return UserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            slogan=user.slogan,
            favorites=user.favorites.split(',')
        )

    def create_or_patch_name(self, token: str, request: PutNameRequest):
        user=self._middleware.get_current_user(token)
        if not user:
            raise UserNotFoundException
        user_request = User(
            name = request.name
        )

        updated_user = self._user_repository.put_user(user.id, user_request)

        return UserResponse(
            id=updated_user.id,
            name=updated_user.name,
            email=updated_user.email,
            slogan=updated_user.slogan,
            favorites=updated_user.favorites.split(',')
        )

    def create_or_patch_slogan(self, token: str, request: PutSloganRequest):
        user=self._middleware.get_current_user(token)
        if not user:
            raise UserNotFoundException
        user_request = User(
            slogan = request.slogan
        )

        updated_user = self._user_repository.put_user(user.id, user_request)

        return UserResponse(
            id=updated_user.id,
            name=updated_user.name,
            email=updated_user.email,
            slogan=updated_user.slogan,
            favorites=updated_user.favorites.split(',')
        )

    def create_or_patch_favorites(self, token: str, request: PutFavoritesRequest):
        if len(request.favorites) > MAX_FAVORITES_SIZE:
            raise InvalidFormException

        user=self._middleware.get_current_user(token)
        if not user:
            raise UserNotFoundException
        user_request = User(
            favorites = ','.join(request.favorites)
        )

        updated_user = self._user_repository.put_user(user.id, user_request)

        return UserResponse(
            id=updated_user.id,
            name=updated_user.name,
            email=updated_user.email,
            slogan=updated_user.slogan,
            favorites=updated_user.favorites.split(',')
        )
