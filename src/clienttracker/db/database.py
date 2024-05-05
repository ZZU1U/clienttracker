# DataBase Base
from ..config import db_url
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine, inspect

sync_engine = create_engine(url=db_url, echo=True)

session_factory = sessionmaker(sync_engine)


class Base(DeclarativeBase):
    pass


def create_tables() -> None:
    Base.metadata.drop_all(sync_engine)
    Base.metadata.create_all(sync_engine)


def init_tables() -> bool:
    if not inspect(sync_engine).has_table("clients") or \
            not inspect(sync_engine).has_table("purchases") or \
            not inspect(sync_engine).has_table("notes"):
        create_tables()
        return False

    return True
