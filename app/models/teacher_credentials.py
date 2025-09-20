from sqlmodel import SQLModel, Field
from datetime import datetime

class TeacherCredentials(SQLModel, table=True):
    __tablename__ = "teacher_credentials"
    
    teacher_id: int = Field(foreign_key="teachers.teacher_id", primary_key=True)
    username: str = Field(max_length=50, unique=True)
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)