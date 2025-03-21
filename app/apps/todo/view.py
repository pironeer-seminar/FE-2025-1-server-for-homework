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
from app.apps.todo.service import TodoService
from app.apps.todo.service import TodoRepository
from app.apps.common.common_exception import InvalidFormException
from app.apps.common.common_exception import UserPermissionDeniedException
from app.apps.middleware.exceptions import InvalidTokenError
from app.apps.todo.schemas import TodoCompleteUpdateRequest
from app.apps.todo.schemas import TodoContentUpdateRequest
from app.apps.todo.schemas import TodoCreateRequest
from app.apps.todo.schemas import TodoResponse

router = APIRouter(prefix="/todos", tags=["todos"])

oauth2_scheme = HTTPBearer()

def get_token(credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    token = credentials.credentials
    if not token:
        raise InvalidTokenError
    return token

def get_todo_service(db_session: Annotated[Session, Depends(get_db_session)]) -> TodoService:
    middleware = get_middleware_service(db_session)
    todo_repository = TodoRepository(db_session)
    return TodoService(todo_repository, middleware)

@router.post("/", response_model=TodoResponse, responses=responses_from(
            InvalidTokenError,
            InvalidFormException,
            UserPermissionDeniedException
        ))
def create_todo(
        request: TodoCreateRequest,
        token: Annotated[str, Depends(get_token)],
        todo_service: Annotated[TodoService, Depends(get_todo_service)]
    ):
    return todo_service.create_todo(token, request)

@router.get("/", response_model=List[TodoResponse], responses=responses_from(
            InvalidTokenError,
            UserPermissionDeniedException
        ))
def get_all_todos(
        token: Annotated[str, Depends(get_token)],
        todo_service: Annotated[TodoService, Depends(get_todo_service)]
    ):
    return todo_service.get_all_todos(token)

@router.patch("/{todo_id}", response_model=TodoResponse, responses=responses_from(
            InvalidTokenError,
            UserPermissionDeniedException
        ))
def update_todo_contents(
        todo_id: str,
        request: TodoContentUpdateRequest,
        token: Annotated[str, Depends(get_token)],
        todo_service: Annotated[TodoService, Depends(get_todo_service)]
    ):
    return todo_service.update_todo_contents(todo_id, request, token)

@router.patch("/completed/{todo_id}", response_model=TodoResponse, responses=responses_from(
            InvalidTokenError,
            UserPermissionDeniedException
        ))
def update_todo_completed(
        todo_id: str,
        request: TodoCompleteUpdateRequest,
        token: Annotated[str, Depends(get_token)],
        todo_service: Annotated[TodoService, Depends(get_todo_service)]
    ):
    return todo_service.update_todo_completed(todo_id, request, token)

@router.delete("/{todo_id}", response_model=TodoResponse)
def delete_todo(
        todo_id: str,
        token: Annotated[str, Depends(get_token)],
        todo_service: Annotated[TodoService, Depends(get_todo_service)]
    ):
    todo_service.delete_todo(todo_id, token)
