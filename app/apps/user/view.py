from typing import Annotated
from typing import List
from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials
from sqlmodel import Session

from app.database import get_db_session
from app.apps.common.exceptions import responses_from
from app.apps.middleware.service import MiddlewareService
from app.apps.user.service import UserService
from app.apps.user.repository import UserRepository
from app.apps.user.exceptions import EmailAlreadyExistsException
from app.apps.user.exceptions import UserAlreadyExistsException
from app.apps.user.exceptions import UserNotFoundException
from app.apps.common.common_exception import InvalidFormException
from app.apps.middleware.exceptions import InvalidTokenError
from app.apps.user.schemas import SignUpRequest
from app.apps.user.schemas import SignInRequest
from app.apps.user.schemas import UserResponse

router = APIRouter(prefix="/users", tags=["users"])

oauth2_scheme = HTTPBearer()

def get_token(credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    token = credentials.credentials
    if not token:
        raise InvalidTokenError
    return token

def get_user_service(db_session: Annotated[Session, Depends(get_db_session)]) -> UserService:
    user_repository = UserRepository(db_session)
    middleware = MiddlewareService(user_repository)
    return UserService(user_repository, middleware)

@router.post("/", responses=responses_from(
            UserAlreadyExistsException,
            EmailAlreadyExistsException,
            InvalidFormException
        ))
def sign_up(request: SignUpRequest, user_service: Annotated[UserService, Depends(get_user_service)]):
    return user_service.sign_up_user(request)

@router.post("/session", responses=responses_from(      
            UserNotFoundException,
            InvalidFormException
        ))
def sign_in(request: SignInRequest, user_service: Annotated[UserService, Depends(get_user_service)]):
    return user_service.sign_in_user(request)

@router.get("/me", responses=responses_from(
            UserNotFoundException,
            InvalidFormException,
            InvalidTokenError
        ))
def get_my_info(
        user_service: Annotated[UserService, Depends(get_user_service)],
        token: Annotated[str, Depends(get_token)]
    ):
    return user_service.get_my_info(token)

@router.get("/users", response_model=List[UserResponse])
def get_users(user_service: Annotated[UserService, Depends(get_user_service)]):
    return user_service.get_all_users()
