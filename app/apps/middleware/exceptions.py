from fastapi import HTTPException

from app.apps.common.exceptions import CustomException

class BlockedTokenError(CustomException):
    def __init__(self):
        super().__init__(status_code=401, detail="만료된 리프레시 토큰입니다.")

class ExpiredSignatureError(CustomException):
    def __init__(self):
        super().__init__(status_code=401, detail="토큰이 만료되었습니다.")

class InvalidTokenError(CustomException):
    def __init__(self):
        super().__init__(status_code=401, detail="유효하지 않은 토큰입니다.")
