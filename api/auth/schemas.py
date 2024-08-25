from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class AccessToken(BaseModel):
    access: str


class RefreshToken(BaseModel):
    refresh: str


class Tokens(AccessToken, RefreshToken):
    type: str = "Bearer"


class LoginData(BaseModel):
    username: str
    password: str


class BaseUser(BaseModel):
    username: str = Field(max_length=50)
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr
    birthday: datetime | None = None
    avatar: str | None = None


class UserOnRegister(BaseUser):
    password: str

    class Config:
        from_attributes = True


class UserInfo(BaseUser):
    id: int
