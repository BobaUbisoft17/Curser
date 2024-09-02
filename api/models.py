"""File to database models."""

from datetime import date, datetime

from sqlalchemy import ForeignKey, JSON, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    first_name: Mapped[str] = mapped_column(String(20), nullable=True)
    last_name: Mapped[str] = mapped_column(String(30), nullable=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    birthday: Mapped[date] = mapped_column(nullable=True)
    first_login: Mapped[datetime] = mapped_column(insert_default=func.now())
    avatar: Mapped[str] = mapped_column(nullable=True)
    password: Mapped[str]

    courses: Mapped[list["Course"]] = relationship(
        back_populates="author",
        cascade="all, delete",
    )


class Course(Base):
    __tablename__ = "course"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str] = mapped_column(String(4096), nullable=True)
    date_started: Mapped[date]
    workload: Mapped[str] = mapped_column(nullable=True)
    language: Mapped[str] = mapped_column(String(20))
    avatar: Mapped[str] = mapped_column(nullable=True)
    chapters_sequense: Mapped[list[int]] = mapped_column(JSON(), insert_default=[], server_default="[]")

    author_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE")
    )
    author: Mapped["User"] = relationship(back_populates="courses")

    reviews: Mapped[list["Review"]] = relationship(cascade="all, delete")

    chapters: Mapped[list["Chapter"]] = relationship(
        back_populates="course",
        cascade="all, delete",
    )


class Review(Base):
    __tablename__ = "review"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(4096))

    author_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE")
    )

    course_id: Mapped[int] = mapped_column(
        ForeignKey("course.id", ondelete="CASCADE")
    )


class Chapter(Base):
    __tablename__ = "chapter"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(4096), nullable=True)
    avatar: Mapped[str] = mapped_column(nullable=True)

    course_id: Mapped[int] = mapped_column(
        ForeignKey("course.id", ondelete="CASCADE")
    )
    course: Mapped["Course"] = relationship(back_populates="chapters")

    lessons: Mapped[list["Lesson"]] = relationship(
        back_populates="chapter",
        cascade="all, delete",
    )


class Lesson(Base):
    __tablename__ = "lesson"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    content: Mapped[str] = mapped_column(String(16384))

    chapter_id: Mapped[int] = mapped_column(
        ForeignKey("chapter.id", ondelete="CASCADE")
    )
    chapter: Mapped["Chapter"] = relationship(back_populates="lessons")


class Comment(Base):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(1024))

    lesson_id: Mapped[int] = mapped_column(
        ForeignKey("lesson.id", ondelete="CASCADE")
    )

    parent_comment_id: Mapped[int] = mapped_column(
        ForeignKey("comment.id", ondelete="CASCADE"), nullable=True
    )

    author_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE")
    )
