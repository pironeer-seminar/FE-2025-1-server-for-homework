from uuid import UUID
from pydantic import BaseModel
from pydantic import Field

from app.apps.common.enums import SectionEnum

class TodoCreateRequest(BaseModel):
    content: str
    section: SectionEnum

class TodoCompleteUpdateRequest(BaseModel):
    is_completed: bool

class TodoContentUpdateRequest(BaseModel):
    content: str

class TodoResponse(BaseModel):
    id: UUID
    content: str
    section: SectionEnum
    is_completed: bool
