from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import UpdateUserProfile
from ..models import User


async def get_user(session: AsyncSession, user_id: int) -> User:
    return await session.scalar(select(User).where(User.id == user_id))


async def delete_user(session: AsyncSession, user_id: int) -> None:
    await session.execute(delete(User).where(User.id == user_id))
    await session.commit()


async def update_user(
    session: AsyncSession, user_id: int, user_data: UpdateUserProfile
) -> User:

    user = await session.scalar(
        update(User)
        .where(User.id == user_id)
        .values(**user_data.model_dump(exclude_unset=True))
        .returning(User)
    )

    await session.commit()

    await session.refresh(user)

    return user
