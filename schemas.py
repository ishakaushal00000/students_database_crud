from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class StudentBase(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    date_of_birth: date
    email: str = Field(min_length=5, max_length=254)
    phone: Optional[str] = Field(default=None, max_length=30)
    course: Optional[str] = Field(default=None, max_length=100)
    address: Optional[str] = Field(default=None, max_length=300)
    enrollment_date: Optional[date] = None

    @field_validator("name", "email")
    @classmethod
    def strip_required_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("This field cannot be empty.")
        return value

    @field_validator("email")
    @classmethod
    def basic_email_format(cls, value: str) -> str:
        if "@" not in value or "." not in value.rsplit("@", 1)[-1]:
            raise ValueError("Enter a valid email address.")
        return value.lower()


class StudentCreate(StudentBase):
    student_id: str = Field(min_length=1, max_length=30)

    @field_validator("student_id")
    @classmethod
    def clean_student_id(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Student ID cannot be empty.")
        return value


class StudentUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    date_of_birth: Optional[date] = None
    email: Optional[str] = Field(default=None, min_length=5, max_length=254)
    phone: Optional[str] = Field(default=None, max_length=30)
    course: Optional[str] = Field(default=None, max_length=100)
    address: Optional[str] = Field(default=None, max_length=300)
    enrollment_date: Optional[date] = None

    @field_validator("name", "email")
    @classmethod
    def strip_optional_text(cls, value):
        if value is None:
            return value
        value = value.strip()
        if not value:
            raise ValueError("This field cannot be empty.")
        return value

    @field_validator("email")
    @classmethod
    def basic_email_format(cls, value):
        if value is not None and ("@" not in value or "." not in value.rsplit("@", 1)[-1]):
            raise ValueError("Enter a valid email address.")
        return value.lower() if value is not None else value


class StudentRead(StudentBase):
    model_config = ConfigDict(from_attributes=True)

    student_id: str
