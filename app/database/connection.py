from typing import Generator
from sqlmodel import Session
from sqlmodel import SQLModel
from sqlmodel import create_engine
from sqlalchemy.engine.base import Engine
from app.database.config import DBConfig

class DBSession:
    def __init__(self, config: DBConfig):
        self._engine: Engine = create_engine(config.url)
        SQLModel.metadata.create_all(self._engine)

    def get_engine(self):
        return self._engine

def get_db_session() -> Generator[Session, None, None]:
    with Session(DBSession(DBConfig()).get_engine()) as session:
        yield session
