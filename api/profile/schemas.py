from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UpdateUserProfile(BaseModel):
    username: str = Field(max_length=50, default=None)
    first_name: str | None = None
    last_name: str | None = None
    birthday: datetime | None = None
    email: EmailStr | None = None
    avatar: str | None = None

    class Config:
        from_attributes = True


class PublicUserProfile(BaseModel):
    id: int
    username: str = Field(max_length=50)
    first_name: str | None = None
    last_name: str | None = None
    birthday: datetime | None = None
    avatar: str | None = None


class UserProfile(PublicUserProfile):
    email: EmailStr
