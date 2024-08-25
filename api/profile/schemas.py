from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class PublicUserProfile(BaseModel):
    id: int
    username: str = Field(max_length=50)
    first_name: str | None = None
    last_name: str | None = None
    birthday: datetime | None = None
    avatar: str | None = None


class UserProfile(PublicUserProfile):
    email: EmailStr
