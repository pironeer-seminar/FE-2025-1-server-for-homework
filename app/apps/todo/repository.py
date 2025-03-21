from uuid import UUID
from typing import List
from sqlalchemy.orm import Session

from app.apps.todo.model import Todo

class TodoRepository:
    def __init__(self, db: Session):
        self._db = db

    def create_todo(self, todo: Todo) -> Todo:
        self._db.add(todo)
        self._db.commit()
        self._db.refresh(todo)
        return todo

    def get_todos(self, user_id: UUID) -> List[Todo]:
        return self._db.query(Todo).filter(Todo.user_id == user_id).all()

    def get_todo_by_id(self, todo_id: UUID) -> Todo:
        return self._db.query(Todo).filter(Todo.id == todo_id).first()

    def update_todo(self, todo_id: UUID, todo: Todo) -> Todo:
        existing_todo = self.get_todo_by_id(todo_id)

        if (todo.content is not None):
            existing_todo.content = todo.content
        if (todo.is_completed is not None):
            existing_todo.is_completed = todo.is_completed

        self._db.commit()
        self._db.refresh(existing_todo)
        return existing_todo

    def delete_todo(self, todo_id: UUID):
        todo = self.get_todo_by_id(todo_id)
        
        if todo:
            self._db.delete(todo)
            self._db.commit()
