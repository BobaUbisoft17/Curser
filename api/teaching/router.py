from typing import Annotated, Any

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from .dependencies import CourseValidOnCreate, CourseValidOnUpdate, IsAuthor
from .schemas import CourseOnCreate, CourseOnAnswer, CourseOnUpdate
from .service import create_course, delete_course, get_course, update_course
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
):
    await delete_course(course_id, session)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
