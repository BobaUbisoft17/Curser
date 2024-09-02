from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import CourseOnCreate, CourseOnUpdate
from ..models import Course


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
    return await session.scalar(
        select(Course).where(Course.id == course_id)
    )


async def update_course(
    course_id: int,
    course_data: CourseOnUpdate,
    session: AsyncSession
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