from datetime import date

from pydantic import BaseModel


class CoursePreview(BaseModel):
    id: int
    name: str
    avatar: str | None


class CourseOnAdmission(BaseModel):
    course_id: int


class AuthorPreview(BaseModel):
    id: int
    username: str
    avatar: str | None


class ChapterPreview(BaseModel):
    id: int
    name: str
    description: str | None
    avatar: str | None


class CourseInfo(CoursePreview):
    description: str | None
    workload: str | None
    date_started: date
    language: str
    chapters_sequense: list[int]
    chapters: list[ChapterPreview]
    author: AuthorPreview


class LessonPreview(BaseModel):
    id: int
    name: str


class LessonInfo(LessonPreview):
    content: str
