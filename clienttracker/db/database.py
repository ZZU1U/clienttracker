from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine

db_path = 'sqlite:///clients.db'

sync_engine = create_engine(
    url=db_path,
    echo=True
)

session_factory = sessionmaker(sync_engine)

class Base(DeclarativeBase):
    pass
