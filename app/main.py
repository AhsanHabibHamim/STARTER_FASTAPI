from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from datetime import date, datetime
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()


# ✅ Updated Student Model (your JSON structure)
class Student(BaseModel):
    id: int
    full_name: str
    email: str
    phone: str
    age: int
    department: str
    cgpa: float
    is_graduated: bool
    admission_date: date
    created_at: datetime
    skills: str
    address: str


# DB connection
try:
    conn = psycopg2.connect(
        host="localhost",
        database="Ahsan",
        user="postgres",
        password="1234",
        cursor_factory=RealDictCursor,
    )

    cursor = conn.cursor()
    print("Database Connected Successfully")

except Exception as error:
    print(error)


# GET all students
@app.get("/")
def read_root():
    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()
    return {"students": data}


# POST new student
@app.post("/students")
def create_student(student: Student):

    cursor.execute(
        """
        INSERT INTO students (
            id,
            full_name,
            email,
            phone,
            age,
            department,
            cgpa,
            is_graduated,
            admission_date,
            created_at,
            skills,
            address
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING *;
        """,
        (
            student.id,
            student.full_name,
            student.email,
            student.phone,
            student.age,
            student.department,
            student.cgpa,
            student.is_graduated,
            student.admission_date,
            student.created_at,
            student.skills,
            student.address,
        ),
    )

    new_student = cursor.fetchone()
    conn.commit()

    return {"message": "Student created successfully", "data": new_student}


@app.get("/students/{id}")
def get_student(id: int):
    cursor.execute("""SELECT * from students where id = %s""", (id,))
    student = cursor.fetchone()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Student not found"
        )
    return {"student": student}


# Update student by id
@app.put("/students/{id}")
def update_student(id: int, student: Student):
    cursor.execute(
        """
        UPDATE students SET
            full_name = %s,
            email = %s,
            phone = %s,
            age = %s,
            department = %s,
            cgpa = %s,
            is_graduated = %s,
            admission_date = %s,
            created_at = %s,
            skills = %s,
            address = %s
        WHERE id = %s
        RETURNING *;
    """,
        (
            student.full_name,
            student.email,
            student.phone,
            student.age,
            student.department,
            student.cgpa,
            student.is_graduated,
            student.admission_date,
            student.created_at,
            student.skills,
            student.address,
            id,
        ),
    )
    updated_student = cursor.fetchone()
    conn.commit()
    if not updated_student:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student updated successfully", "data": updated_student}


# Delete student by id
@app.delete("/students/{id}")
def delete_student(id: int):
    cursor.execute("DELETE FROM students WHERE id = %s RETURNING *;", (id,))
    deleted_student = cursor.fetchone()
    conn.commit()
    if not deleted_student:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully", "data": deleted_student}
