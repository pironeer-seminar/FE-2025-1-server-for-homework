import os
import bcrypt
import jwt
import uuid
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
from app.apps.common.schemas import TokenRequest
from app.apps.user.exceptions import EmailAlreadyExistsException
from app.apps.user.exceptions import UserAlreadyExistsException
from app.apps.user.exceptions import UserNotFoundException
from app.apps.user.exceptions import UserPermissionDeniedException
from app.apps.middleware.exceptions import InvalidTokenError
from app.apps.common.common_exception import InvalidFormException

class UserService:
    def __init__(self, user_repository: UserRepository, middleware: MiddlewareService):
        self._user_repository = user_repository
        self._middleware = middleware

    def _hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

    def _issue_token(self, id: uuid.UUID) -> tuple[str, str]:
        access_payload = {
            "sub": str(id),
            "exp": datetime.now() + timedelta(minutes=5),
            "typ": TokenType.ACCESS.value,
        }
        access_token = jwt.encode(access_payload, os.getenv("JWT_SECRET_KEY"), algorithm="HS256")

        return access_token

    # TODO: 토큰 재발급 로직 만들기
    # def _reissue_token(self, refresh_token: str) -> tuple[str, str]:
    #     id = self._middleware.validate_refresh_token(refresh_token)
    #     self.user_repository.block_token(refresh_token, datetime.now())        
    #     refresh_payload = {
    #         "sub": id,
    #         "jti": uuid4().hex,
    #         "exp": datetime.now() + timedelta(days=7),
    #         "typ": TokenType.REFRESH.value,
    #     }
    #     refresh_token = jwt.encode(refresh_payload, os.getenv("JWT_SECRET_KEY"), algorithm="HS256")
    #     access_token = self._issue_token(id)
    #     return access_token, refresh_token

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
        if not User:
            raise UserNotFoundException
        return UserResponse(id=user.id, name=user.name, email=user.email)

    def get_all_users(self) -> List[User]:
        users = self._user_repository.get_users()
        return [UserResponse(id=user.id, name=user.name, email=user.email) for user in users]
