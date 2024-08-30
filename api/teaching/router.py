from typing import Annotated, Any

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .dependencies import CourseDataIsValid
from .schemas import CourseOnCreate
from .service import create_course
from ..auth.dependencies import DatabaseSession, IsAuthenticated


router = APIRouter(prefix="/teach", tags=["Teach"])


@router.post("/course")
async def create_course_handler(
    payload: Annotated[dict[str, Any], Depends(IsAuthenticated())],
    course_data: Annotated[CourseOnCreate, Depends(CourseDataIsValid())],
    session: Annotated[AsyncSession, Depends(DatabaseSession())],
):
    return await create_course(course_data, payload["id"], session)
