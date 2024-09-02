from datetime import date

from pydantic import BaseModel, Field


class BaseCourse(BaseModel):
    description: str | None = Field(max_length=4096, default=None)
    workload: str | None = None
    language: str = Field(max_length=20)
    avatar: str | None = None


class CourseOnCreate(BaseCourse):
    name: str = Field(max_length=64)
    date_started: date


class CourseOnUpdate(BaseCourse):
    name: str | None = Field(max_length=64, default=None)
    date_started: date | None = None
    chapters_sequense: list[int] = []


class CourseOnAnswer(CourseOnCreate):
    id: int
    chapters_sequense: list[int]


class CourseDataForVerification(BaseModel):
    name: str | None = Field(max_length=64, default=None)
    date_started: date | None = None