from datetime import date

from pydantic import BaseModel, Field


class CourseOnCreate(BaseModel):
    name: str = Field(max_length=64)
    description: str | None = Field(max_length=4096, default=None)
    date_started: date
    workload: str | None = None
    language: str = Field(max_length=20)
    avatar: str | None = None
