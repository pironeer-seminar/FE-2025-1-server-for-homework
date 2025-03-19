from typing import Annotated
from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlmodel import Session
from app.database import get_db_session
from app.apps.user.model import User
from app.apps.user.service import UserService
from app.apps.user.repository import UserRepository

router = APIRouter(prefix="/users", tags=["users"])

def get_user_service(db_session: Annotated[Session, Depends(get_db_session)]) -> UserService:
    user_repository = UserRepository(db_session)
    return UserService(user_repository)

@router.get("/users", response_model=List[User])
def get_users(user_service: Annotated[UserService, Depends(get_user_service)]):
    return user_service.get_all_users()

@router.get("/users/{user_id}", response_model=User)
def get_user(user_id: int, user_service: Annotated[UserService, Depends(get_user_service)]):
    user = user_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user