from fastapi import HTTPException, status


CourseDoesNotExist = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Course doesn't exist"
)


ChapterDoesNotExist = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Chapter doesn't exist"
)


UserHasNotAccess = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="User has not access"
)


ReviewDoesNotExist = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Review doesn't exist"
)