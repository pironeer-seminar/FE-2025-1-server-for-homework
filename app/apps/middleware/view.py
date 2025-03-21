from typing import Annotated
from sqlmodel import Session
from fastapi import Depends

from app.database import get_db_session
from app.apps.middleware.service import MiddlewareService
from app.apps.user.service import UserRepository

def get_middleware_service(db_session: Annotated[Session, Depends(get_db_session)]) -> MiddlewareService:
    user_repository = UserRepository(db_session)
    return MiddlewareService(user_repository)
