from app.apps.common.exceptions import CustomException

class TodoNotFoundException(CustomException):
    def __init__(self):
        super().__init__(status_code=404, detail="존재하지 않는 유저입니다.")

