import uuid
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(..., max_length=30)
    email: str = Field(..., index=True, sa_column_kwargs={"unique": True})
    password: str = Field(..., max_length=255)

    class Config:
        json_encoders = {uuid.UUID: str}
