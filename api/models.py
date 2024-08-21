from datetime import date, datetime
from sqlalchemy import ForeignKey, func, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(String(50), unique=True)
    first_name: Mapped[str] = mapped_column(String(20), nullable=True)
    last_name: Mapped[str] = mapped_column(String(30), nullable=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=True)
    birthday: Mapped[date]
    first_login: Mapped[datetime] = mapped_column(insert_default=func.now())
    avatar: Mapped[str]
    password: Mapped[str]

    courses: Mapped[list["Course"]] = relationship(back_populates="author")


class Course(Base):
    __tablename__ = "course"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str] = mapped_column(String(4096), nullable=True)
    reviews: Mapped[float]
    date_started: Mapped[date]
    workload: Mapped[str]
    language: Mapped[str] = mapped_column(String(20))
    avatar: Mapped[str]

    author_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    author: Mapped["User"] = relationship(back_populates="courses")
 