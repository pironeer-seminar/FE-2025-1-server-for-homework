from typing import Annotated
from typing import List
from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials
from sqlmodel import Session

from app.database import get_db_session
from app.apps.common.exceptions import responses_from
from app.apps.middleware.view import get_middleware_service
from app.apps.user.service import UserService
from app.apps.user.service import UserRepository
from app.apps.user.exceptions import EmailAlreadyExistsException
from app.apps.user.exceptions import UserAlreadyExistsException
from app.apps.user.exceptions import UserNotFoundException
from app.apps.common.common_exception import InvalidFormException
from app.apps.middleware.exceptions import InvalidTokenError
from app.apps.user.schemas import SignUpRequest
from app.apps.user.schemas import SignInRequest
from app.apps.user.schemas import UserWithToken
from app.apps.user.schemas import UserResponse
from app.apps.user.schemas import PutNameRequest
from app.apps.user.schemas import PutSloganRequest
from app.apps.user.schemas import PutFavoritesRequest

router = APIRouter(prefix="/users", tags=["users"])

oauth2_scheme = HTTPBearer()

def get_token(credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    token = credentials.credentials
    if not token:
        raise InvalidTokenError
    return token

def get_user_service(db_session: Annotated[Session, Depends(get_db_session)]) -> UserService:
    middleware = get_middleware_service(db_session)
    user_repository = UserRepository(db_session)
    return UserService(user_repository, middleware)

@router.post("/", response_model=UserWithToken, responses=responses_from(
            UserAlreadyExistsException,
            EmailAlreadyExistsException,
            InvalidFormException
        ))
def sign_up(request: SignUpRequest, user_service: Annotated[UserService, Depends(get_user_service)]):
    return user_service.sign_up_user(request)

@router.post("/session", response_model=UserWithToken, responses=responses_from(      
            UserNotFoundException,
            InvalidFormException
        ))
def sign_in(request: SignInRequest, user_service: Annotated[UserService, Depends(get_user_service)]):
    return user_service.sign_in_user(request)

@router.get("/me", response_model=UserResponse, responses=responses_from(
            UserNotFoundException,
            InvalidFormException,
            InvalidTokenError
        ))
def get_my_info(
        user_service: Annotated[UserService, Depends(get_user_service)],
        token: Annotated[str, Depends(get_token)]
    ):
    return user_service.get_my_info(token)

@router.put("/profile/name", response_model=UserResponse)
def create_or_patch_name(
        token: Annotated[str, Depends(get_token)],
        request: PutNameRequest,
        user_service: Annotated[UserService, Depends(get_user_service)]
    ):
    return user_service.create_or_patch_name(token, request)

@router.put("profile/slogan", response_model=UserResponse)
def create_or_patch_slogan(
        token: Annotated[str, Depends(get_token)],
        request: PutSloganRequest,
        user_service: Annotated[UserService, Depends(get_user_service)]
    ):
    return user_service.create_or_patch_slogan(token, request)

@router.put("/profile/favorites", response_model=UserResponse)
def create_or_patch_favorites(
        token: Annotated[str, Depends(get_token)],
        request: PutFavoritesRequest,
        user_service: Annotated[UserService, Depends(get_user_service)]
    ):
    return user_service.create_or_patch_favorites(token, request)
