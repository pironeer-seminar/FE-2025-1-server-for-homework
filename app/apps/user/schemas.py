import re
import uuid
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field
from pydantic import field_validator

class SignUpRequest(BaseModel):
    name: str = Field(..., max_length=30)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=64)

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if not re.search(r"[A-Z]", value):
            raise ValueError("비밀번호에는 최소 1개의 대문자가 포함되어야 합니다.")
        if not re.search(r"[a-z]", value):
            raise ValueError("비밀번호에는 최소 1개의 소문자가 포함되어야 합니다.")
        if not re.search(r"\d", value):
            raise ValueError("비밀번호에는 최소 1개의 숫자가 포함되어야 합니다.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("비밀번호에는 최소 1개의 특수문자가 포함되어야 합니다.")
        if " " in value:
            raise ValueError("비밀번호에는 공백을 포함할 수 없습니다.")
        return value

class SignInRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=64)

class UserWithToken(BaseModel):
    id: uuid.UUID
    name: str = Field(..., max_length=30)
    email: EmailStr
    token: str

class UserResponse(BaseModel):
    id: uuid.UUID
    name: str = Field(..., max_length=30)
    email: EmailStr
