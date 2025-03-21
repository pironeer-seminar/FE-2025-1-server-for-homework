from fastapi import HTTPException

from app.apps.common.exceptions import CustomException

class InvalidFormException(CustomException):
    def __init__(self):
        super().__init__(status_code=400, detail="유효하지 않은 폼 요청입니다.")

class UserPermissionDeniedException(CustomException):
    def __init__(self):
        super().__init__(status_code=403, detail="권한이 없습니다.")

class InvalidUUIDException(CustomException):
    def __init__(self):
        super().__init__(status_code=403, detail="아이디가 유효하지 않습니다.")
