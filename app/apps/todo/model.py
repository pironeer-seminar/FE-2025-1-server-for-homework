from uuid import UUID
from uuid import uuid4
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

from app.apps.common.enums import SectionEnum
from app.apps.user.model import User

class Todo(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    content: str = Field(..., max_length=100)
    is_completed: bool = Field(default=False)
    section: SectionEnum = Field(..., index=True)
    user_id: UUID = Field(foreign_key="user.id")

