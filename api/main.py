"""Entry point."""

from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

from .auth.router import router as auth_router
from .auth.token_service import AuthJWT
from .config import Config
from .database import Database
from .middlewares import DatabaseMiddleware, JWTMiddleware, S3Middleware
from .profile.router import router as profile_router
from ..s3.minio import S3Service


class Memourse:
    def __init__(self) -> None:
        config = Config(_env_file=".env")

        db = Database(config.DBURL)
        auth_jwt = AuthJWT(config.SECRETKEY, config.JWTALGORITHM)
        s3_service = S3Service(
            config.BUCKETNAME,
            config.ENDPOINT,
            config.ACCESS_KEY,
            config.SECRETKEYS3
        )

        self.db_middleware = DatabaseMiddleware(db.session)
        self.jwt_middlware = JWTMiddleware(auth_jwt)
        self.s3_middleware = S3Middleware(s3_service)

    def create_app(self) -> FastAPI:
        app = FastAPI()
        app.include_router(auth_router)
        app.include_router(profile_router)
        app.add_middleware(BaseHTTPMiddleware, dispatch=self.db_middleware)
        app.add_middleware(BaseHTTPMiddleware, dispatch=self.jwt_middlware)
        app.add_middleware(BaseHTTPMiddleware, dispatch=self.s3_middleware)
        return app


memourse = Memourse()
