from datetime import date
from typing import Optional

from fastapi import FastAPI, Depends, HTTPException, Query, Response, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Student
from schemas import StudentCreate, StudentRead, StudentUpdate

# Create the SQLite tables the first time the application starts.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Students Database CRUD API",
    description=(
        "A beginner-friendly student record management API built with "
        "FastAPI and SQLite. Use /docs to test all endpoints."
    ),
    version="1.0.0",
)

# Useful if a separate frontend is added later. For production, restrict origins.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Home"])
def home():
    return {
        "message": "Welcome to the Students Database CRUD API",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}


@app.post(
    "/students",
    response_model=StudentRead,
    status_code=status.HTTP_201_CREATED,
    tags=["Students"],
    summary="Create a student",
)
def create_student(payload: StudentCreate, db: Session = Depends(get_db)):
    existing = db.get(Student, payload.student_id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Student ID '{payload.student_id}' already exists.",
        )

    student = Student(**payload.model_dump())
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


@app.get("/students", response_model=list[StudentRead], tags=["Students"])
def list_students(
    search: Optional[str] = Query(
        default=None, description="Search name, email, phone, or course"
    ),
    course: Optional[str] = Query(default=None, description="Filter by course"),
    born_after: Optional[date] = Query(
        default=None, description="Only students born on/after YYYY-MM-DD"
    ),
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    statement = select(Student)

    if search:
        term = f"%{search.strip()}%"
        statement = statement.where(
            or_(
                Student.name.ilike(term),
                Student.email.ilike(term),
                Student.phone.ilike(term),
                Student.course.ilike(term),
            )
        )
    if course:
        statement = statement.where(Student.course.ilike(f"%{course.strip()}%"))
    if born_after:
        statement = statement.where(Student.date_of_birth >= born_after)

    statement = statement.order_by(Student.name.asc()).offset(offset).limit(limit)
    return list(db.scalars(statement).all())


@app.get(
    "/students/{student_id}",
    response_model=StudentRead,
    tags=["Students"],
    summary="Get one student",
)
def get_student(student_id: str, db: Session = Depends(get_db)):
    student = db.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found.")
    return student


@app.put(
    "/students/{student_id}",
    response_model=StudentRead,
    tags=["Students"],
    summary="Replace a student's details",
)
def replace_student(
    student_id: str, payload: StudentCreate, db: Session = Depends(get_db)
):
    student = db.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found.")
    if payload.student_id != student_id:
        raise HTTPException(
            status_code=400,
            detail="The student_id in the body must match the URL student_id.",
        )

    for field, value in payload.model_dump().items():
        setattr(student, field, value)

    db.commit()
    db.refresh(student)
    return student


@app.patch(
    "/students/{student_id}",
    response_model=StudentRead,
    tags=["Students"],
    summary="Update selected student fields",
)
def update_student(
    student_id: str, payload: StudentUpdate, db: Session = Depends(get_db)
):
    student = db.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found.")

    changes = payload.model_dump(exclude_unset=True)
    if not changes:
        raise HTTPException(status_code=400, detail="No update fields were provided.")

    for field, value in changes.items():
        setattr(student, field, value)

    db.commit()
    db.refresh(student)
    return student


@app.delete(
    "/students/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Students"],
    summary="Delete a student",
)
def delete_student(student_id: str, db: Session = Depends(get_db)):
    student = db.get(Student, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found.")
    db.delete(student)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
