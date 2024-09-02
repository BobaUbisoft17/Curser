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


class BaseChapter(BaseModel):
    description: str | None = Field(max_length=4096, default=None)
    avatar: str | None = None


class ChapterOnCreate(BaseChapter):
    name: str = Field(max_length=100)


class ChapterOnUpdate(BaseChapter):
    name: str | None = Field(max_length=100, default=None)
    lessons_sequence: list[int] = []


class ChapterOnAnswer(ChapterOnCreate):
    id: int
    lessons_sequence: list[int] = []


class LessonOnCreate(BaseModel):
    name: str = Field(max_length=50)
    content: str = Field(max_length=16384)


class LessonOnUpdate(BaseModel):
    name: str | None = Field(max_length=50, default=None)
    content: str | None = Field(max_length=16384, default=None)


class LessonOnAnswer(LessonOnCreate):
    id: int
