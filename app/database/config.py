import os 

class DBConfig():
    def __init__(self):
        self.username: str = os.getenv("DB_USERNAME")
        self.password: str = os.getenv("DB_PASSWORD")
        self.host: str = os.getenv("DB_HOST")
        self.port: int = int(os.getenv("DB_PORT"))
        self.name: str = os.getenv("DB_NAME")

    @property
    def url(self) -> str:
        return (
            f"mysql+mysqldb://{self.username}:{self.password}"
            f"@{self.host}:{self.port}/{self.name}"
            "?charset=utf8mb4"
        )
