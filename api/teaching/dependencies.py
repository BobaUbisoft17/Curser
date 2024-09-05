from datetime import date
from typing import Annotated, Any

from fastapi import Depends
from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from .exceptions import CourseNameIsTaken, DateIsIncorrect, InsufficientRights
from .schemas import CourseDataForVerification, CourseOnCreate, CourseOnUpdate
from ..auth.dependencies import DatabaseSession, IsAuthenticated
from ..models import Chapter, Course, Lesson


class CourseValidOnUpdate:

    async def __call__(
        self,
        course_data: CourseOnUpdate,
        session: Annotated[AsyncSession, Depends(DatabaseSession())],
    ) -> CourseOnUpdate:
        return await CourseDataIsValid(session, course_data).validate()


class CourseValidOnCreate:

    async def __call__(
        self,
        course_data: CourseOnCreate,
        session: Annotated[AsyncSession, Depends(DatabaseSession())],
    ) -> CourseOnCreate:
        return await CourseDataIsValid(session, course_data).validate()


class CourseDataIsValid:

    def __init__(
        self, session: AsyncSession, course_data: CourseDataForVerification
    ):
        self.session = session
        self.course_data = course_data

    async def validate(self) -> CourseDataForVerification:
        if (
            self.course_data.name is not None
            and await self.course_name_is_not_available()
        ):
            raise CourseNameIsTaken

        if self.course_data.date_started is not None and self.date_is_valid():
            raise DateIsIncorrect

        return self.course_data

    async def course_name_is_not_available(self) -> bool:
        return await self.session.scalar(
            select(exists().where(Course.name == self.course_data.name))
        )

    def date_is_valid(self) -> bool:
        return self.course_data.date_started < date.today()


class IsCourseAuthor:

    async def __call__(
        self,
        course_id: int,
        payload: Annotated[dict[str, Any], Depends(IsAuthenticated())],
        session: Annotated[AsyncSession, Depends(DatabaseSession())],
    ) -> int:
        if not await session.scalar(
            select(
                exists().where(
                    Course.id == course_id, Course.author_id == payload["id"]
                )
            )
        ):
            raise InsufficientRights
        return course_id


class IsChapterAuthor:

    async def __call__(
        self,
        chapter_id: int,
        course_id: Annotated[int, Depends(IsCourseAuthor())],
        session: Annotated[AsyncSession, Depends(DatabaseSession())],
    ) -> int:
        if not await session.scalar(
            select(
                exists().where(
                    Chapter.course_id == course_id, Chapter.id == chapter_id
                )
            )
        ):
            raise InsufficientRights
        return chapter_id


class IsLessonAuthor:

    async def __call__(
        self,
        lesson_id: int,
        chapter_id: Annotated[int, Depends(IsChapterAuthor())],
        session: Annotated[AsyncSession, Depends(DatabaseSession())],
    ) -> None:
        if not await session.scalar(
            select(
                exists().where(
                    Lesson.chapter_id == chapter_id, Lesson.id == lesson_id
                )
            )
        ):
            raise InsufficientRights
