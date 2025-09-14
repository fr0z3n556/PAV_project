from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class TeacherCreate(BaseModel):
    full_name: str
    photo_path: Optional[str] = None

class TeacherRead(BaseModel):
    teacher_id: int
    full_name: str
    photo_path: Optional[str] = None

class TeacherUpdate(BaseModel):
    full_name: Optional[str] = None
    photo_path: Optional[str] = None

class TeacherCredentialsCreate(BaseModel):
    username: str
    password: str

class TeacherCredentialsRead(BaseModel):
    username: str
    created_at: datetime

class LoginRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None  