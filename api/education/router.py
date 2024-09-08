from typing import Annotated, Any

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from .dependencies import (
    CommentIsExist,
    CommentIsValid,
    CourseExistBody,
    CourseExistPathParam,
    HasAccessToChapter,
    HasAccessToCourse,
    HasAccessToLesson,
    IsCommentAuthor,
    IsReviewAuthor,
)
from .schemas import CommentOnAnswer, CommentOnCreate, CommentOnUpdate, CourseInfo, CoursePreview, LessonInfo, LessonPreview, ReviewOnAnswer, ReviewOnCreate, ReviewOnUpdate
from .service import (
    add_course_for_education,
    create_comment,
    create_review,
    delete_comment,
    delete_review,
    get_comments,
    get_course_info,
    get_course_reviews,
    get_lesson,
    get_lessons,
    get_subcomments,
    get_user_courses,
    update_comment,
    update_reveiw,
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


@router.get("/course/{course_id}/reviews", dependencies=[Depends(IsAuthenticated())])
async def get_course_reviews_handler(
    course_id: Annotated[int, Depends(CourseExistPathParam())],
    session: Annotated[AsyncSession, Depends(DatabaseSession())]
) -> list[ReviewOnAnswer]:
    return await get_course_reviews(course_id, session)


@router.post("/review")
async def create_review_handler(
    review: Annotated[ReviewOnCreate, Depends(HasAccessToCourse())],
    payload: Annotated[dict[str, Any], Depends(IsAuthenticated())],
    session: Annotated[AsyncSession, Depends(DatabaseSession())]
) -> ReviewOnAnswer:
    return await create_review(review, payload["id"], session)


@router.put("/review/{review_id}")
async def update_review_handler(
    review_id: Annotated[int, Depends(IsReviewAuthor())],
    review_data: ReviewOnUpdate,
    session: Annotated[AsyncSession, Depends(DatabaseSession())]
) -> ReviewOnAnswer:
    return await update_reveiw(review_id, review_data, session)


@router.delete("/review/{review_id}")
async def delete_review_handler(
    review_id: Annotated[int, Depends(IsReviewAuthor())],
    session: Annotated[AsyncSession, Depends(DatabaseSession())]
) -> Response:
    
    await delete_review(review_id, session)
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/lesson/{lesson_id}/comments", dependencies=[Depends(IsAuthenticated())])
async def get_comments_handler(
    lesson_id: Annotated[int, Depends(HasAccessToLesson())],
    session: Annotated[AsyncSession, Depends(DatabaseSession())]
) -> list[CommentOnAnswer]:
    return await get_comments(lesson_id, session)



@router.post("/lesson/{lesson_id}/comment")
async def create_comment_handler(
    comment: Annotated[CommentOnCreate, Depends(CommentIsValid())],
    lesson_id: int,
    payload: Annotated[dict[str, Any], Depends(IsAuthenticated())],
    session: Annotated[AsyncSession, Depends(DatabaseSession())]
) -> CommentOnAnswer:
    return await create_comment(comment, lesson_id, payload["id"], session)


@router.get("/comment/{comment_id}/subcomments")
async def get_subcomments_handler(
    comment_id: Annotated[int, Depends(CommentIsExist())],
    session: Annotated[AsyncSession, Depends(DatabaseSession())]
) -> list[CommentOnAnswer]:
    return await get_subcomments(comment_id, session)


@router.put("/comment/{comment_id}")
async def update_comment_handler(
    comment_id: Annotated[int, Depends(IsCommentAuthor())],
    comment_changes: CommentOnUpdate,
    session: Annotated[AsyncSession, Depends(DatabaseSession())]
) -> CommentOnAnswer:
    return await update_comment(comment_id, comment_changes, session)


@router.delete("/comment/{comment_id}")
async def delete_comment_handler(
    comment_id: Annotated[int, Depends(IsCommentAuthor())],
    session: Annotated[AsyncSession, Depends(DatabaseSession())]
) -> Response:
    await delete_comment(comment_id, session)
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)