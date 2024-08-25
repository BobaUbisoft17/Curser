from typing import Annotated, Any

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from .exceptions import InvalidPasswordOrUsername
from .schemas import LoginData, RefreshToken, UserOnRegister
from .service import get_user, user_is_valid
from .token_service import AuthJWT, TokenVerification
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


class RefreshConfiscationAgent:
    async def __call__(self, token: RefreshToken) -> str:
        return token.refresh


class TokenIsRefresh:
    async def __call__(
        self,
        token: Annotated[str, Depends(RefreshConfiscationAgent())],
        jwt_service: Annotated[AuthJWT, Depends(JWTServcie())],
    ) -> dict[str, Any]:
        payload = TokenVerification("refresh", jwt_service).validate_token(
            token
        )
        return payload


class IsAuthenticated:
    async def __call__(
        self,
        token: Annotated[str, Depends(auth_scheme)],
        jwt_service: Annotated[AuthJWT, Depends(JWTServcie())],
    ) -> Any:
        return TokenVerification("access", jwt_service).validate_token(
            token
        )
