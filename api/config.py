"""File for load config data."""

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    SECRETKEY: str = "SECRETKEY"
    DBURL: str = "sqlite+aiosqlite:///sql_app.db"
    JWTALGORITHM: str = ""
    BUCKETNAME: str = "test.bucket"
    ENDPOINT: str = "http://localhost:9000"
    ACCESS_KEY: str = "test_access_key"
    SECRETKEYS3: str = "test_password"
    