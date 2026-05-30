from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from datetime import date, datetime
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models
from sqlalchemy.orm import Session
from .database import engine, get_db

app = FastAPI()


models.Base.metadata.create_all(bind=engine)

# ===This is Our Get Method===
@app.get("/studentalchemy")
def getStudent(db: Session = Depends(get_db)):
    return {"Status": "SQL ALCHEMY Working"}

# ===This is Our Post Method===
@app.post("addStudent")
def addStudent():
    pass


# ===This is Our Update Method===
@app.put("addStudent")
def updateStudent():
    pass


# ===This is Our Delete Method===
@app.delete("addStudent")
def deleteStudent():
    pass

