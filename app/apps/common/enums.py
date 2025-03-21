from enum import Enum

class TokenType(Enum):
    ACCESS = "access"
    REFRESH = "refresh"

class SectionEnum(str, Enum):
    SCHOOL = "SCHOOL"
    PIRONEER = "PIRONEER"
    PERSONAL = "PERSONAL"
