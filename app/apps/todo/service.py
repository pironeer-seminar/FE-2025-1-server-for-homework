from uuid import UUID

from app.apps.middleware.service import MiddlewareService
from app.apps.todo.repository import TodoRepository
from app.apps.todo.repository import Todo
from app.apps.todo.schemas import TodoCreateRequest
from app.apps.todo.schemas import TodoContentUpdateRequest
from app.apps.todo.schemas import TodoCompleteUpdateRequest
from app.apps.todo.schemas import TodoResponse
from app.apps.todo.exceptions import TodoNotFoundException
from app.apps.user.exceptions import UserNotFoundException
from app.apps.common.common_exception import InvalidFormException
from app.apps.common.common_exception import UserPermissionDeniedException
from app.apps.common.common_exception import InvalidUUIDException

class TodoService:
    def __init__(self, todo_repository: TodoRepository, middleware: MiddlewareService):
        self._todo_repository = todo_repository
        self._middleware = middleware

    def create_todo(self, token: str, request: TodoCreateRequest):
        user = self._middleware.get_current_user(token)
        todo_request = Todo(
            content = request.content,
            is_completed = False,
            section = request.section,
            user_id = user.id
        )

        try:
            todo = self._todo_repository.create_todo(todo_request)
        except ValueError as exc:
            raise InvalidFormException from exc

        return TodoResponse(
                id=todo.id,
                content=todo.content,
                section=todo.section,
                is_completed=todo.is_completed,
            )

    def get_all_todos(self, token: str):
        user = self._middleware.get_current_user(token)
        if not user:
            raise UserNotFoundException

        todos = self._todo_repository.get_todos(user.id)
        return [TodoResponse(
                    id=todo.id,
                    content=todo.content,
                    is_completed=todo.is_completed,
                    section=todo.section
                ) for todo in todos]

    def update_todo_contents(self, todo_id: str, request: TodoContentUpdateRequest, token: str):
        user = self._middleware.get_current_user(token)
        try:
            todo_uuid_id = UUID(todo_id)
        except ValueError as exc:
            raise InvalidUUIDException from exc

        todo = self._todo_repository.get_todo_by_id(todo_uuid_id)
        if not todo:
            raise TodoNotFoundException
        if user.id != todo.user_id:
            raise UserPermissionDeniedException

        todo_request = Todo(
            content = request.content,
        )
        updated_todo = self._todo_repository.update_todo(todo_uuid_id, todo_request)

        return TodoResponse(
                id=updated_todo.id,
                content=updated_todo.content,
                is_completed=updated_todo.is_completed,
                section=updated_todo.section
            )

    def update_todo_completed(self, todo_id: str, request: TodoCompleteUpdateRequest, token: str):
        user = self._middleware.get_current_user(token)

        try:
            todo_uuid_id = UUID(todo_id)
        except ValueError as exc:
            raise InvalidUUIDException from exc
        todo = self._todo_repository.get_todo_by_id(todo_uuid_id)
    
        if not todo:
            raise TodoNotFoundException
        if user.id != todo.user_id:
            raise UserPermissionDeniedException

        todo_request = Todo(
            is_completed = request.is_completed,
        )
        updated_todo = self._todo_repository.update_todo(todo_uuid_id, todo_request)

        return TodoResponse(
                id=updated_todo.id,
                content=updated_todo.content,
                is_completed=updated_todo.is_completed,
                section=updated_todo.section
            )

    def delete_todo(self, todo_id: str, token: str):
        user = self._middleware.get_current_user(token)

        try:
            todo_uuid_id = UUID(todo_id)
        except ValueError as exc:
            raise InvalidUUIDException from exc

        todo = self._todo_repository.get_todo_by_id(todo_uuid_id)
        if not todo:
            raise TodoNotFoundException

        if user.id != todo.user_id:
            raise UserPermissionDeniedException

        self._todo_repository.delete_todo(todo_uuid_id)

