from typing import Annotated, Any

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .dependencies import (
    DatabaseSession,
    JWTServcie,
    TokenIsRefresh,
    UserExist,
    UserNotExist,
)
from .schemas import AccessToken, Tokens, UserInfo, UserOnRegister
from .service import create_user
from .token_service import AuthJWT
from ..models import User

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/jwt/create")
async def get_token(
    user: Annotated[User, Depends(UserExist())],
    jwt_service: Annotated[AuthJWT, Depends(JWTServcie())],
) -> Tokens:

    payload = {
        "id": user.id,
        "username": user.username,
        "email": user.email
    }
    return Tokens(
        access=jwt_service.create_access_token(payload),
        refresh=jwt_service.create_refresh_token(payload),
    )


@router.post("/jwt/refresh")
async def refresh_token(
    payload: Annotated[dict[str, Any], Depends(TokenIsRefresh())],
    jwt_service: Annotated[AuthJWT, Depends(JWTServcie())],
) -> AccessToken:

    return AccessToken(access=jwt_service.create_access_token(payload))


@router.post("/register")
async def register_user(
    user_info: Annotated[UserOnRegister, Depends(UserNotExist())],
    session: Annotated[AsyncSession, Depends(DatabaseSession())],
) -> UserInfo:

    return await create_user(user_info, session)
