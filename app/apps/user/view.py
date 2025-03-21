from typing import Annotated
from typing import List
from fastapi import APIRouter
from fastapi import Depends
from sqlmodel import Session

from app.database import get_db_session
from app.apps.common.exceptions import responses_from
from app.apps.user.service import UserService
from app.apps.user.repository import UserRepository
from app.apps.user.exceptions import EmailAlreadyExistsException
from app.apps.user.exceptions import UserAlreadyExistsException
from app.apps.user.exceptions import UserNotFoundException
from app.apps.user.exceptions import UserPermissionDeniedException
from app.apps.common.common_exception import InvalidFormException
from app.apps.user.schemas import SignUpRequest
from app.apps.user.schemas import SignInRequest
from app.apps.common.schemas import TokenRequest
from app.apps.user.model import User

router = APIRouter(prefix="/users", tags=["users"])

def get_user_service(db_session: Annotated[Session, Depends(get_db_session)]) -> UserService:
    user_repository = UserRepository(db_session)
    return UserService(user_repository)

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

# @router.get("/me", responses=responses_from(
#             UserPermissionDeniedException,
#             UserNotFoundException,
#             InvalidFormException
#         ))
# def get_my_info(request: TokenRequest, user_service: Annotated[UserService, Depends(get_user_service)]):
#     return user_service.get_my_info(request)
@router.get("/users", response_model=List[User])
def get_users(user_service: Annotated[UserService, Depends(get_user_service)]):
    return user_service.get_all_users()
