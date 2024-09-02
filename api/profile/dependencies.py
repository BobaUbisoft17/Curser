from typing import Annotated, Any

from fastapi import Depends
from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from .exceptions import EmailIsTaken, UsernameIsTaken
from .schemas import UpdateUserProfile
from ..auth.dependencies import DatabaseSession, IsAuthenticated
from ..models import User


class UserDataIsValid:
    async def __call__(
        self,
        user_data: UpdateUserProfile,
        session: Annotated[AsyncSession, Depends(DatabaseSession())],
        _: Annotated[Any, Depends(IsAuthenticated())],
    ) -> UpdateUserProfile:
        if not await self.username_is_available(user_data.username, session):
            raise UsernameIsTaken

        if not await self.email_is_available(user_data.email, session):
            raise EmailIsTaken

        return user_data

    async def username_is_available(
        self, username: str | None, session: AsyncSession
    ) -> bool:
        if username is None:
            return True

        return not await session.scalar(
            select(exists().where(User.username == username))
        )

    async def email_is_available(
        self, email: str | None, session: AsyncSession
    ) -> bool:
        if email is None:
            return True

        return not await session.scalar(
            select(exists().where(User.email == email))
        )
