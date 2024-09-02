from typing import Annotated, Any

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from .dependencies import UserDataIsValid
from .exceptions import UserDoesNotExist
from .schemas import PublicUserProfile, UpdateUserProfile, UserProfile
from .service import delete_user, get_user, update_user
from ..auth.dependencies import DatabaseSession, IsAuthenticated


router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("")
async def get_user_profile(
    payload: Annotated[dict[str, Any], Depends(IsAuthenticated())],
    session: Annotated[AsyncSession, Depends(DatabaseSession())],
) -> UserProfile:

    user = await get_user(session, payload["id"])
    if user is None:
        raise UserDoesNotExist

    return user


@router.put("")
async def update_user_data(
    new_user_data: Annotated[UpdateUserProfile, Depends(UserDataIsValid())],
    payload: Annotated[dict[str, Any], Depends(IsAuthenticated())],
    session: Annotated[AsyncSession, Depends(DatabaseSession())],
) -> UserProfile:
    return await update_user(session, payload["id"], new_user_data)


@router.delete("")
async def delete_user_data(
    payload: Annotated[dict[str, Any], Depends(IsAuthenticated())],
    session: Annotated[AsyncSession, Depends(DatabaseSession())],
) -> Response:
    await delete_user(session, payload["id"])
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/{user_id}", dependencies=[Depends(IsAuthenticated())])
async def get_user_public_profile(
    user_id: int, session: Annotated[AsyncSession, Depends(DatabaseSession())]
) -> PublicUserProfile:

    user = await get_user(session, user_id)
    if user is None:
        raise UserDoesNotExist

    return user
