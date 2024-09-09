from passlib.context import CryptContext
from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import LoginData, UserOnRegister
from ..models import User


pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Authorization:

    @staticmethod
    def password_is_valid(password: str, user_password: str) -> bool:
        return pwd.verify(password, user_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd.hash(password)


async def get_user(login_data: LoginData, session: AsyncSession) -> User:
    user = await session.scalar(
        select(User).where(
            User.username == login_data.username,
        )
    )
    if Authorization.password_is_valid(login_data.password, user.password):
        return user
    return None


async def user_is_valid(
    user_info: UserOnRegister, session: AsyncSession
) -> tuple[bool, str]:

    if await email_exist(user_info.email, session):
        return False, "Email is in use by another user"

    if await username_exist(user_info.username, session):
        return False, "Username is in use by another user"

    return True, ""


async def email_exist(email: str, session: AsyncSession) -> bool:
    st = select(exists(User).where(User.email == email))
    return await session.scalar(st)


async def username_exist(username: str, session: AsyncSession) -> bool:
    st = select(exists(User).where(User.username == username))
    return await session.scalar(st)


async def create_user(
    user_info: UserOnRegister, session: AsyncSession
) -> User:

    user_info.password = Authorization.get_password_hash(user_info.password)
    user = User(**user_info.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
