from datetime import date, datetime
from sqlalchemy import func, String
from sqlalchemy.orm import Mapped, mapped_column

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
