from typing import Annotated, Any

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from .dependencies import (
    CourseExistBody,
    CourseExistPathParam,
    HasAccessToChapter,
    HasAccessToLesson,
)
from .schemas import CourseInfo, CoursePreview, LessonInfo, LessonPreview
from .service import (
    add_course_for_education,
    get_course_info,
    get_lesson,
    get_lessons,
    get_user_courses,
)
from ..auth.dependencies import DatabaseSession, IsAuthenticated


router = APIRouter(
    prefix="/education",
    tags=["Education"],
)


@router.get("/courses")
async def get_courses_handler(
    payload: Annotated[dict[str, Any], Depends(IsAuthenticated())],
    session: Annotated[AsyncSession, Depends(DatabaseSession())],
) -> list[CoursePreview]:
    return await get_user_courses(payload["id"], session)


@router.post("/add-course")
async def add_course_handler(
    course_id: Annotated[int, Depends(CourseExistBody())],
    payload: Annotated[dict[str, Any], Depends(IsAuthenticated())],
    session: Annotated[AsyncSession, Depends(DatabaseSession())],
) -> Response:
    await add_course_for_education(payload["id"], course_id, session)

    return Response(status_code=status.HTTP_201_CREATED)


@router.get("/course/{course_id}", dependencies=[Depends(IsAuthenticated())])
async def get_course_handler(
    course_id: Annotated[int, Depends(CourseExistPathParam())],
    session: Annotated[AsyncSession, Depends(DatabaseSession())],
) -> CourseInfo:
    return await get_course_info(course_id, session)


@router.get(
    "/chapter/{chapter_id}/lessons", dependencies=[Depends(IsAuthenticated())]
)
async def get_lessons_handler(
    chapter_id: Annotated[int, Depends(HasAccessToChapter())],
    session: Annotated[AsyncSession, Depends(DatabaseSession())],
) -> list[LessonPreview]:
    return await get_lessons(chapter_id, session)


@router.get("/lesson/{lesson_id}", dependencies=[Depends(IsAuthenticated())])
async def get_lesson_handler(
    lesson_id: Annotated[int, Depends(HasAccessToLesson())],
    session: Annotated[AsyncSession, Depends(DatabaseSession())],
) -> LessonInfo:
    return await get_lesson(lesson_id, session)


# @router.post("/review")
# async def create_review_handler():
#    ...
#
#
# @router.post("/comment")
# async def create_comment_handler():
#    ...
#
