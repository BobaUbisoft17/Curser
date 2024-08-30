from typing import Annotated

from fastapi import Depends
from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from .exceptions import CourseNameIsTaken
from .schemas import CourseOnCreate
from ..auth.dependencies import DatabaseSession
from ..models import Course


class CourseDataIsValid:

    async def __call__(
        self,
        course_data: CourseOnCreate,
        session: Annotated[AsyncSession, Depends(DatabaseSession())],
    ) -> CourseOnCreate:
        if await self.course_name_is_not_available(course_data.name, session):
            raise CourseNameIsTaken
        return course_data

    async def course_name_is_not_available(
        self, course_name: str, session: AsyncSession
    ) -> bool:
        return await session.scalar(
            select(exists().where(Course.name == course_name))
        )
