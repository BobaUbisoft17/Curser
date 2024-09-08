from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .service import get_courses
from ..auth.dependencies import DatabaseSession, IsAuthenticated
from ..education.schemas import CoursePreview


router = APIRouter(prefix="/catalog", tags=["Catalog"])


@router.get("", dependencies=[Depends(IsAuthenticated())])
async def get_courses_handler(
    session: Annotated[AsyncSession, Depends(DatabaseSession())]
) -> list[CoursePreview]:
    return await get_courses(session)
