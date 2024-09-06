from typing import Annotated, Any

from fastapi import Depends
from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from .exceptions import (
    ChapterDoesNotExist,
    CourseDoesNotExist,
    ReviewDoesNotExist,
    UserHasNotAccess,
)
from .models import UserCourse
from .schemas import CourseOnAdmission, ReviewOnCreate
from ..auth.dependencies import DatabaseSession, IsAuthenticated
from ..models import Chapter, Course, Lesson, Review


class CourseExistBody:

    async def __call__(
        self,
        course: CourseOnAdmission,
        session: Annotated[AsyncSession, Depends(DatabaseSession())],
    ) -> int:
        if not await session.scalar(
            select(exists().where(Course.id == course.course_id))
        ):
            raise CourseDoesNotExist
        return course.course_id


class CourseExistPathParam:

    async def __call__(
        self,
        course_id: int,
        session: Annotated[AsyncSession, Depends(DatabaseSession())],
    ) -> int:
        if not await session.scalar(
            select(exists().where(Course.id == course_id))
        ):
            raise CourseDoesNotExist
        return course_id


class ChapterExist:

    async def __call__(
        self,
        chapter_id: int,
        session: Annotated[AsyncSession, Depends(DatabaseSession())],
    ) -> int:
        if not await session.scalar(
            select(Chapter).where(Chapter.id == chapter_id)
        ):
            raise ChapterDoesNotExist
        return chapter_id


class HasAccessToChapter:

    async def __call__(
        self,
        payload: Annotated[dict[str, Any], Depends(IsAuthenticated())],
        chapter_id: Annotated[int, Depends(ChapterExist())],
        session: Annotated[AsyncSession, Depends(DatabaseSession())],
    ) -> int:
        course_id = (
            select(Chapter.id)
            .where(Chapter.id == chapter_id)
            .scalar_subquery()
        )
        if not await session.scalar(
            select(
                exists().where(
                    UserCourse.user_id == payload["id"],
                    UserCourse.course_id == course_id,
                )
            )
        ):
            raise UserHasNotAccess
        return chapter_id


class LessonExist:

    async def __call__(
        self,
        lesson_id: int,
        session: Annotated[AsyncSession, Depends(DatabaseSession())],
    ) -> int:
        if not await session.scalar(
            select(Lesson).where(Lesson.id == lesson_id)
        ):
            raise ChapterDoesNotExist
        return lesson_id


class HasAccessToLesson:

    async def __call__(
        self,
        lesson_id: Annotated[int, Depends(LessonExist())],
        paylaod: Annotated[dict[str, Any], Depends(IsAuthenticated())],
        session: Annotated[AsyncSession, Depends(DatabaseSession())],
    ) -> int:
        chapter_id = (
            select(Lesson.chapter_id)
            .where(Lesson.id == lesson_id)
            .scalar_subquery()
        )
        course_id = (
            select(Chapter.course_id)
            .where(Chapter.id == chapter_id)
            .scalar_subquery()
        )
        if not await session.scalar(
            select(
                exists().where(
                    UserCourse.user_id == paylaod["id"],
                    UserCourse.course_id == course_id,
                )
            )
        ):
            raise UserHasNotAccess
        return lesson_id


class HasAccessToCourse:

    async def __call__(
        self,
        review: ReviewOnCreate,
        course_id: Annotated[int, Depends(CourseExistBody())],
        payload: Annotated[dict[str, Any], Depends(IsAuthenticated())],
        session: Annotated[AsyncSession, Depends(DatabaseSession())]
    ) -> ReviewOnCreate:
        if not await session.scalar(
            select(exists().where(UserCourse.user_id == payload["id"], UserCourse.course_id == course_id))
        ):
            raise UserHasNotAccess
        return review


class ReviewIsExist:

    async def __call__(
        self,
        review_id: int,
        session: Annotated[AsyncSession, Depends(DatabaseSession())]
    ) -> int:
        if not await session.scalar(
            select(exists().where(Review.id == review_id))
        ):
            raise ReviewDoesNotExist
        return review_id


class IsReviewAuthor:

    async def __call__(
        self,
        review_id: Annotated[int, Depends(ReviewIsExist())],
        payload: Annotated[dict[str, Any], Depends(IsAuthenticated())],
        session: Annotated[AsyncSession, Depends(DatabaseSession())] 
    ) -> int:
        if not await session.scalar(
            select(exists().where(Review.id == review_id, Review.author_id == payload["id"]))
        ):
            raise UserHasNotAccess
        return review_id