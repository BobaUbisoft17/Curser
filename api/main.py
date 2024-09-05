"""Entry point."""

from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

from .auth.router import router as auth_router
from .auth.token_service import AuthJWT
from .config import Config
from .database import Database
from .education.router import router as education_router
from .middlewares import DatabaseMiddleware, JWTMiddleware
from .profile.router import router as profile_router
from .teaching.router import router as teaching_router


class Memourse:
    def __init__(self) -> None:
        config = Config(_env_file=".env")

        db = Database(config.DBURL)
        auth_jwt = AuthJWT(config.SECRETKEY, config.JWTALGORITHM)

        self.db_middleware = DatabaseMiddleware(db.session)
        self.jwt_middlware = JWTMiddleware(auth_jwt)

    def create_app(self) -> FastAPI:
        app = FastAPI()

        app.include_router(auth_router)
        app.include_router(profile_router)
        app.include_router(teaching_router)
        app.include_router(education_router)

        app.add_middleware(BaseHTTPMiddleware, dispatch=self.db_middleware)
        app.add_middleware(BaseHTTPMiddleware, dispatch=self.jwt_middlware)
        return app


memourse = Memourse()
