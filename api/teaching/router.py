from typing import Annotated, Any

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from .dependencies import CourseValidOnCreate, CourseValidOnUpdate, IsAuthor
from .schemas import (
    ChapterOnAnswer,
    ChapterOnCreate,
    ChapterOnUpdate,
    CourseOnAnswer,
    CourseOnCreate,
    CourseOnUpdate,
)
from .service import (
    create_chapter,
    create_course,
    delete_chapter,
    delete_course,
    get_chapters,
    get_course,
    update_chapter,
    update_course,
)
from ..auth.dependencies import DatabaseSession, IsAuthenticated


router = APIRouter(prefix="/teach", tags=["Teach"])


@router.post("/course")
async def create_course_handler(
    payload: Annotated[dict[str, Any], Depends(IsAuthenticated())],
    course_data: Annotated[CourseOnCreate, Depends(CourseValidOnCreate())],
    session: Annotated[AsyncSession, Depends(DatabaseSession())],
) -> CourseOnAnswer:
    return await create_course(course_data, payload["id"], session)


@router.get("/course/{course_id}", dependencies=[Depends(IsAuthor())])
async def get_course_handler(
    course_id: int,
    session: Annotated[AsyncSession, Depends(DatabaseSession())],
) -> CourseOnAnswer:
    return await get_course(course_id, session)


@router.put("/course/{course_id}", dependencies=[Depends(IsAuthor())])
async def change_course_handler(
    course_id: int,
    course_changes: Annotated[CourseOnUpdate, Depends(CourseValidOnUpdate())],
    session: Annotated[AsyncSession, Depends(DatabaseSession())],
) -> CourseOnAnswer:
    return await update_course(course_id, course_changes, session)


@router.delete("/course/{course_id}", dependencies=[Depends(IsAuthor())])
async def delete_course_handler(
    course_id: int,
    session: Annotated[AsyncSession, Depends(DatabaseSession())],
) -> Response:
    await delete_course(course_id, session)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/course/{course_id}/chapter", dependencies=[Depends(IsAuthor())])
async def create_chapter_handler(
    course_id: int,
    chapter_data: ChapterOnCreate,
    session: Annotated[AsyncSession, Depends(DatabaseSession())],
) -> ChapterOnAnswer:
    return await create_chapter(course_id, chapter_data, session)


@router.get("/course/{course_id}/chapters", dependencies=[Depends(IsAuthor())])
async def get_chapters_handler(
    course_id: int,
    session: Annotated[AsyncSession, Depends(DatabaseSession())],
) -> list[ChapterOnAnswer]:
    return await get_chapters(course_id, session)


@router.put(
    "/course/{course_id}/chapter/{chapter_id}",
    dependencies=[Depends(IsAuthor())],
)
async def update_chapter_handler(
    chapter_id: int,
    chapter_changes: ChapterOnUpdate,
    session: Annotated[AsyncSession, Depends(DatabaseSession())],
) -> ChapterOnAnswer:
    return await update_chapter(chapter_id, chapter_changes, session)


@router.delete(
    "/course/{course_id}/chapter/{chapter_id}",
    dependencies=[Depends(IsAuthor())],
)
async def delete_chapter_handler(
    chapter_id: int,
    session: Annotated[AsyncSession, Depends(DatabaseSession())],
) -> Response:
    await delete_chapter(chapter_id, session)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
