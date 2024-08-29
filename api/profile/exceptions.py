from fastapi import HTTPException, status


UserDoesNotExist = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User does not exist"
)


UsernameIsTaken = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Username is taken"
)


EmailIsTaken = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Email is taken"
)
