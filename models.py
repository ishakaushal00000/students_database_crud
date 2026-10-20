from sqlalchemy import Date, String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Student(Base):
    __tablename__ = "students"

    # Student ID is supplied by the user and must be unique.
    student_id: Mapped[str] = mapped_column(String(30), primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    date_of_birth: Mapped[object] = mapped_column(Date, nullable=False)
    email: Mapped[str] = mapped_column(String(254), nullable=False, index=True)
    phone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    course: Mapped[str | None] = mapped_column(String(100), nullable=True)
    address: Mapped[str | None] = mapped_column(String(300), nullable=True)
    enrollment_date: Mapped[object | None] = mapped_column(Date, nullable=True)
