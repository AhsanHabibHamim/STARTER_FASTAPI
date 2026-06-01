from pydantic import BaseModel, EmailStr
from datetime import datetime


class createUser(BaseModel):
    email: EmailStr
    password: str
