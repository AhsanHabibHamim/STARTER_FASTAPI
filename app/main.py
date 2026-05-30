from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from datetime import date, datetime
from . import models
from sqlalchemy.orm import Session
from .database import engine, get_db

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


# ===>>Students Base Model<<===
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


# ===>>This is Our Get Method<<===
@app.get("/allStudents")
def getStudent(db: Session = Depends(get_db)):
    students = db.query(models.Student).all()
    return {"Students_Details": students}


# ===>>This is Our Dynamic Getting Method<<===
@app.get("/student/{id}")
def getOneStudent(id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Student not found"
        )
    return {"Students_Details_According_To_ID": student}


# ===>>This is Our Post Method<<===
@app.post("/addStudent", status_code=status.HTTP_201_CREATED)
def addStudent(student: Student, db: Session = Depends(get_db)):
    new_student = models.Student(
        id=student.id,
        full_name=student.full_name,
        email=student.email,
        phone=student.phone,
        age=student.age,
        department=student.department,
        cgpa=student.cgpa,
        is_graduated=student.is_graduated,
        admission_date=student.admission_date,
        created_at=student.created_at,
        skills=student.skills,
        address=student.address,
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return {"NEW STUDENT": new_student}


# ===>>This is Our Update Method<<===
@app.put("/updateStudent/{id}")
def updateStudent(id: int, updated_data: Student, db: Session = Depends(get_db)):
    student_query = db.query(models.Student).filter(models.Student.id == id)
    student = student_query.first()

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with id {id} not found",
        )

    student_query.update({models.Student.__table__.c[k]: v for k, v in updated_data.model_dump().items()}, synchronize_session=False)
    db.commit()

    return {"UPDATED STUDENT": student_query.first()}


# ===>>This is Our Delete Method<<===
@app.delete("/deleteStudent/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deleteStudent(id: int, db: Session = Depends(get_db)):
    student_query = db.query(models.Student).filter(models.Student.id == id)
    student = student_query.first()

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with id {id} not found",
        )

    student_query.delete(synchronize_session=False)
    db.commit()
    return {"message": f"Student with id {id} deleted successfully"}
