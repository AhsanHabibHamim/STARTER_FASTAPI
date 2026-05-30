from sqlalchemy import Column, Integer, Float, String, Boolean, Date, DateTime
from .database import Base


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    department = Column(String, nullable=False)
    cgpa = Column(Float, nullable=False)
    is_graduated = Column(Boolean, nullable=False)
    admission_date = Column(Date, nullable=False)
    created_at = Column(DateTime, nullable=False)
    skills = Column(String, nullable=False)
    address = Column(String, nullable=False)
