from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Course


async def get_courses(session: AsyncSession) -> list[Course]:
    return await session.scalars(select(Course))
