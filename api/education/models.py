from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base
from ..models import Course


class UserCourse(Base):
    __tablename__ = "user_course"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("course.id", ondelete="CASCADE"), primary_key=True)

    courses: Mapped[list[Course]] = relationship(cascade="all, delete")
