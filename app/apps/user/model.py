from uuid import UUID
from uuid import uuid4
from sqlmodel import SQLModel
from sqlmodel import Field
from typing import List
from typing import Optional

class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(..., max_length=30)
    email: str = Field(..., index=True, sa_column_kwargs={"unique": True})
    password: str = Field(..., max_length=255)

    slogan: Optional[str] = Field(default=None, max_length=200)
    favorites: Optional[str] = Field(default=None, max_length=2048)
