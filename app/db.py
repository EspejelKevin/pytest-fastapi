from contextlib import contextmanager, suppress
from typing import Iterator

from sqlalchemy import Engine
from sqlmodel import Session, create_engine


class Database:
    def __init__(self, uri: str, **options: dict) -> None:
        self.__engine = create_engine(uri, connect_args=options)
        self.__session = Session(self.__engine)

    def __enter__(self):
        return self

    def get_engine(self) -> Engine:
        return self.__engine

    def get_session(self) -> Session:
        return self.__session

    def __exit__(self, exception_type, exception_value, traceback):
        self.client.close()


class SQLiteDatabase:
    def __init__(self, uri: str, **options: dict) -> None:
        self.__database = Database(uri, **options)

    @contextmanager
    def session(self) -> Iterator[Database]:
        with suppress(Exception):
            yield self.__database

    def engine(self) -> Engine:
        return self.__database.get_engine()
