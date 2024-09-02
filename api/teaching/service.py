from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import (
    ChapterOnCreate,
    ChapterOnUpdate,
    CourseOnCreate,
    CourseOnUpdate,
    LessonOnCreate,
    LessonOnUpdate,
)
from ..models import Chapter, Course, Lesson


async def create_course(
    course_data: CourseOnCreate, author_id: int, session: AsyncSession
) -> Course:
    course = Course(
        **course_data.model_dump(exclude_unset=True), author_id=author_id
    )
    session.add(course)
    await session.commit()
    await session.refresh(course)
    return course


async def get_course(course_id: int, session: AsyncSession) -> Course:
    return await session.scalar(select(Course).where(Course.id == course_id))


async def update_course(
    course_id: int, course_data: CourseOnUpdate, session: AsyncSession
) -> Course:
    course = await session.scalar(
        update(Course)
        .where(Course.id == course_id)
        .values(**course_data.model_dump(exclude_unset=True))
        .returning(Course)
    )

    await session.commit()
    await session.refresh(course)

    return course


async def delete_course(course_id: int, session: AsyncSession) -> None:
    await session.execute(delete(Course).where(Course.id == course_id))
    await session.commit()


async def create_chapter(
    course_id: int, chapter_data: ChapterOnCreate, session: AsyncSession
) -> Chapter:
    chapter = Chapter(
        **chapter_data.model_dump(exclude_unset=True), course_id=course_id
    )
    session.add(chapter)

    await session.commit()
    await session.refresh(chapter)

    return chapter


async def get_chapters(course_id: int, session: AsyncSession) -> list[Chapter]:
    return await session.scalars(
        select(Chapter).where(Chapter.course_id == course_id)
    )


async def update_chapter(
    chapter_id: int, chapter_changes: ChapterOnUpdate, session: AsyncSession
) -> Chapter:
    chapter = await session.scalar(
        update(Chapter)
        .where(Chapter.id == chapter_id)
        .values(**chapter_changes.model_dump(exclude_unset=True))
        .returning(Chapter)
    )

    await session.commit()

    await session.refresh(chapter)
    return chapter


async def delete_chapter(chapter_id: int, session: AsyncSession) -> None:
    await session.execute(delete(Chapter).where(Chapter.id == chapter_id))
    await session.commit()


async def create_lesson(
    chapter_id: int, lesson: LessonOnCreate, session: AsyncSession
) -> Lesson:
    lesson = Lesson(
        **lesson.model_dump(exclude_unset=True), chapter_id=chapter_id
    )
    session.add(lesson)
    await session.commit()
    await session.refresh(lesson)

    return lesson


async def get_lessons(chapter_id: int, session: AsyncSession) -> list[Lesson]:
    return await session.scalars(
        select(Lesson).where(Lesson.chapter_id == chapter_id)
    )


async def update_lesson(
    lesson_id: int, lesson_changes: LessonOnUpdate, session: AsyncSession
) -> Lesson:
    lesson = await session.scalar(
        update(Lesson)
        .where(Lesson.id == lesson_id)
        .values(**lesson_changes.model_dump(exclude_unset=True))
        .returning(Lesson)
    )

    await session.commit()
    await session.refresh(lesson)

    return lesson


async def delete_lesson(lesson_id: int, session: AsyncSession) -> None:
    await session.execute(delete(Lesson).where(Lesson.id == lesson_id))
    await session.commit()
