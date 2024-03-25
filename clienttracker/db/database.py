# DataBase Base
from clienttracker.config import db_url
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine

sync_engine = create_engine(url=db_url, echo=False)

session_factory = sessionmaker(sync_engine)


class Base(DeclarativeBase):
    pass
