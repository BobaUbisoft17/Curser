"""File for connect with database."""

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Database:
    def __init__(self, db_url: str) -> None:
        self.engine = create_async_engine(
            db_url, connect_args={"check_same_thread": False}
        )
        self.session = async_sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )
