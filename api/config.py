"""File for load config data."""

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    SECRETKEY: str = "SECRETKEY"
    DBURL: str = "sqlite+aiosqlite:///sql_app.db"
    JWTALGORITHM: str = "HSA256"
