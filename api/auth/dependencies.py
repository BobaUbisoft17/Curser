from calendar import timegm
from datetime import datetime
from typing import Annotated, Any

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from .exceptions import InvalidPasswordOrUsername, InvalidToken
from .schemas import LoginData, RefreshToken, UserOnRegister
from .service import get_user, user_is_valid
from .token_service import AuthJWT
from ..models import User


auth_scheme = OAuth2PasswordBearer(tokenUrl="jwt/create")


class DatabaseSession:
    async def __call__(self, request: Request) -> AsyncSession:
        return request.state.session


class JWTServcie:
    async def __call__(self, request: Request) -> AuthJWT:
        return request.state.jwt_service


class UserExist:
    async def __call__(
        self,
        login_data: LoginData,
        session: Annotated[AsyncSession, Depends(DatabaseSession())],
    ) -> User:
        user = await get_user(login_data, session)
        if user is None:
            raise InvalidPasswordOrUsername
        return user


class UserNotExist:
    async def __call__(
        self,
        user_info: UserOnRegister,
        session: Annotated[AsyncSession, Depends(DatabaseSession())],
    ) -> UserOnRegister:

        user_valid, message = await user_is_valid(user_info, session)
        if not user_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=message,
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user_info


class TokenIsDecrypted:
    async def __call__(
        self,
        token: RefreshToken,
        jwt_service: Annotated[AuthJWT, Depends(JWTServcie())],
    ) -> dict[str, Any]:

        payload = jwt_service.decode_token(token.refresh)
        if payload.get("type") is None or payload.get("username") is None:
            raise InvalidToken
        return payload


class TokenIsActive:
    async def __call__(
        self, payload: Annotated[dict[str, Any], Depends(TokenIsDecrypted())]
    ) -> dict[str, Any]:

        if payload["exp"] < timegm(datetime.now().utctimetuple()):
            raise InvalidToken
        return payload


class TokenIsRefresh:
    async def __call__(
        self, payload: Annotated[dict[str, Any], Depends(TokenIsActive())]
    ) -> dict[str, Any]:

        if payload.get("type") != "refresh":
            raise InvalidToken
        return payload
