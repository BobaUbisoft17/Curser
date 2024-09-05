from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from .models import UserCourse
from ..models import Course, Lesson


async def get_user_courses(
    user_id: int, session: AsyncSession
) -> list[Course]:
    return await session.scalars(
        select(UserCourse)
        .where(UserCourse.user_id == user_id)
        .options(joinedload(UserCourse.courses))
    )


async def add_course_for_education(
    user_id: int, course_id: int, session: AsyncSession
) -> None:
    session.add(UserCourse(user_id=user_id, course_id=course_id))
    await session.commit()


async def get_course_info(course_id: int, session: AsyncSession) -> Course:
    return await session.scalar(
        select(Course)
        .where(Course.id == course_id)
        .options(joinedload(Course.chapters), joinedload(Course.author))
    )


async def get_lessons(chapter_id: int, session: AsyncSession) -> list[Lesson]:
    return await session.scalars(
        select(Lesson).where(Lesson.chapter_id == chapter_id)
    )


async def get_lesson(lesson_id: int, session: AsyncSession) -> Lesson:
    return await session.scalar(select(Lesson).where(Lesson.id == lesson_id))
