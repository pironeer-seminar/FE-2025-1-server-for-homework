from typing import Any

from fastapi import HTTPException

class CustomException(HTTPException):
    def __init__(self, status_code: int | None = None, detail: str = ""):
        assert status_code is not None, "status_code must be set"
        super().__init__(status_code=status_code, detail=detail)

    def to_response(self) -> dict[int | str, dict[str, Any]]:
        example = {
            "detail": self.detail,
        }
        return {
            self.status_code: {
                "description": self.__class__.__name__,
                "content": {
                    "application/json": {
                        "example": example,
                    },
                },
            },
        }

def responses_from(
    *exceptions: type[CustomException],
) -> dict[int | str, dict[str, Any]]:
    responses = {}
    for exc in exceptions:
        responses.update(exc().to_response())
    return responses
