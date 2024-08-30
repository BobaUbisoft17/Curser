from fastapi import HTTPException, status


CourseNameIsTaken = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Course name is taken"
)
