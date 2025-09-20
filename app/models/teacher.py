from sqlmodel import SQLModel, Field
from typing import Optional

class Teacher(SQLModel, table=True):
    __tablename__ = "teachers"
    
    teacher_id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str = Field(max_length=100)
    photo_path: Optional[str] = None