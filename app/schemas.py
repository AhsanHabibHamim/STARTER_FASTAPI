from pydantic import BaseModel
from datetime import datetime


class UserCreate(BaseModel):
    id = str
    email = str
    password = str
    created_at = datetime
