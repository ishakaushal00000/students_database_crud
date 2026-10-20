# Students Database CRUD Application

A beginner-friendly Python backend project built with **FastAPI** and **SQLite** for managing student records. It implements Create, Read, Update and Delete (CRUD) operations and provides interactive API documentation.

## Features

- Create student records with a unique student ID
- List all students
- Search by name, email, phone or course
- Filter by course or date of birth
- Retrieve one student by ID
- Replace all student details (`PUT`)
- Update selected details (`PATCH`)
- Delete a student
- Input validation and helpful HTTP error responses
- SQLite persistence: records remain saved after restarting the app
- Interactive API documentation at `/docs`

## Technology stack

- Python 3.10+
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Uvicorn

## Project structure

```text
students_database_crud/
├── main.py
├── database.py
├── models.py
├── schemas.py
├── requirements.txt
├── .gitignore
└── README.md
```

The `students.db` database file is created automatically when the app starts. It is intentionally excluded from Git because it is a local runtime database.

## Installation and run

### 1. Install Python

Install Python 3.10 or newer from https://www.python.org/downloads/. On Windows, enable **Add Python to PATH** during installation.

### 2. Open a terminal in this project folder

In VS Code, open this folder and choose **Terminal → New Terminal**.

### 3. Create and activate a virtual environment (recommended)

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt:

```bat
.venv\Scripts\activate.bat
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Start the API

```bash
uvicorn main:app --reload
```

Open these addresses in your browser:

- Home: http://127.0.0.1:8000/
- Interactive API docs: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

Keep the terminal running while testing the API. Press `Ctrl+C` to stop it.

## Test the API in `/docs`

Open `http://127.0.0.1:8000/docs`, expand an endpoint, click **Try it out**, enter the example request body, and click **Execute**.

### Create a student — `POST /students`

```json
{
  "student_id": "STU001",
  "name": "Aarav Sharma",
  "date_of_birth": "2005-04-12",
  "email": "aarav@example.com",
  "phone": "9876543210",
  "course": "BCA",
  "address": "Dehradun",
  "enrollment_date": "2026-08-01"
}
```

Use dummy data only. Do not enter real students' personal information in a public demo.

### List students — `GET /students`

No request body is required. Optional query examples:

- `/students?course=BCA`
- `/students?search=Aarav`
- `/students?born_after=2005-01-01`
- `/students?limit=20&offset=0`

### Retrieve one student — `GET /students/STU001`

Replace `STU001` with the student ID you created.

### Update selected fields — `PATCH /students/STU001`

```json
{
  "phone": "9999999999",
  "course": "BSc Computer Science"
}
```

### Replace all details — `PUT /students/STU001`

Send the full student object, including the same `student_id` as the URL.

### Delete — `DELETE /students/STU001`

Use a student ID that exists. A successful delete returns HTTP `204 No Content`.

## Main HTTP status codes

| Status | Meaning |
|---|---|
| `200 OK` | Read or update succeeded |
| `201 Created` | Student created |
| `204 No Content` | Student deleted |
| `400 Bad Request` | Invalid update request |
| `404 Not Found` | Student ID does not exist |
| `409 Conflict` | Student ID already exists |
| `422 Unprocessable Entity` | Input validation failed |

## Database design

The `students` table contains:

| Field | Type | Description |
|---|---|---|
| `student_id` | Text, primary key | Unique student ID |
| `name` | Text | Student's name |
| `date_of_birth` | Date | Date of birth |
| `email` | Text | Contact email |
| `phone` | Text, optional | Contact phone |
| `course` | Text, optional | Course/program |
| `address` | Text, optional | Address |
| `enrollment_date` | Date, optional | Enrollment date |

## GitHub submission

1. Create a new repository on https://github.com/new.
2. Upload the **extracted project files** (not the ZIP file itself).
3. Do not upload `.venv`, secrets, or a real database containing personal data.
4. Commit the files.
5. Copy the repository URL into the internship form's **GitHub Link** field.

## Notes

- The project is a local API by default; it is not publicly hosted until deployed.
- The optional Ollama AI extension is not included because the assignment says it is not mandatory.
- This is an educational starter project. Before production use, add authentication, stricter email validation, controlled CORS origins, and deployment/security configuration.
