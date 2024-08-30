from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import CourseOnCreate
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
