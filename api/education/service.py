from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from .schemas import ReviewOnCreate, ReviewOnUpdate
from .models import UserCourse
from ..models import Course, Lesson, Review


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


async def get_course_reviews(course_id: int, session: AsyncSession) -> list[Review]:
    return await session.scalars(
        select(Review).where(Review.course_id == course_id)
    )


async def create_review(review: ReviewOnCreate, author_id: int, session: AsyncSession) -> Review:
    review_obj = await session.scalar(
        insert(Review)
        .values(**review.model_dump(), author_id=author_id)
        .returning(Review).options(joinedload(Review.author))
    )

    await session.commit()
    await session.refresh(review_obj)
    return review_obj


async def update_reveiw(review_id: int, review_changes: ReviewOnUpdate, session: AsyncSession) -> Review:
    review = await session.scalar(
        update(Review)
        .where(Review.id == review_id)
        .values(**review_changes.model_dump())
        .returning(Review).options(joinedload(Review.author))
    )

    await session.commit()
    await session.refresh(review)

    return review


async def delete_review(review_id: int, session: AsyncSession) -> None:
    await session.execute(
        delete(Review).where(Review.id == review_id)
    )

    await session.commit()