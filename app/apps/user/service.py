import bcrypt
from typing import List
from sqlalchemy.exc import IntegrityError

from app.apps.user.repository import UserRepository
from app.apps.user.model import User
from app.apps.user.schemas import SignUpRequest
from app.apps.user.schemas import SignInRequest
from app.apps.user.schemas import UserWithToken
from app.apps.user.schemas import UserResponse
from app.apps.common.schemas import TokenRequest
from app.apps.user.exceptions import EmailAlreadyExistsException
from app.apps.user.exceptions import UserAlreadyExistsException
from app.apps.user.exceptions import UserNotFoundException
from app.apps.user.exceptions import UserPermissionDeniedException
from app.apps.common.common_exception import InvalidFormException

class UserService:
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository
    
    def _hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

    def sign_up_user(self, request: SignUpRequest):
        if self._user_repository.get_by_email(request.email):
            raise EmailAlreadyExistsException()

        hashed_password = self._hash_password(request.password)

        user = User(
            name=request.name,
            email=request.email,
            password=hashed_password,
        )
        try:
            user = self._user_repository.create_user(user)
            # TODO: 토큰 생성 로직 추가
            token = ""
        except ValueError as exc:
            raise InvalidFormException from exc
        except IntegrityError as exc:
            raise UserAlreadyExistsException from exc
        return UserWithToken(name=user.name, email=user.email, token=token)

    def sign_in_user(self, request: SignInRequest):
        user = self._user_repository.get_by_email(request.email)
        if not user:
            raise UserNotFoundException
        
        if not self._verify_password(request.password, user.password):
            raise UserPermissionDeniedException
        
        # TODO: JWT 인증 로직 추가
        token = ""
        return UserWithToken(name=user.name, email=user.email, token=token)

    # def get_my_info(self, request: TokenRequest):
    #     user = self._user_repository.get_by_token(request)
    #     if not User:
    #         raise UserNotFoundException
    #     return UserResponse(id=user.id, name=user.name, email=user.email)

    def get_all_users(self) -> List[User]:
        return self._user_repository.get_users()