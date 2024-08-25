from fastapi import HTTPException, status


UserDoesNotExist = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User does not exist"
)
