from sqlmodel import SQLModel, Field
from typing import Optional

class Discipline(SQLModel, table=True):
    __tablename__ = "disciplines"
    
    discipline_code: str = Field(max_length=20, primary_key=True)
    discipline_name: str = Field(max_length=100)
    theory_hours: Optional[int] = Field(default=0, ge=0)
    practice_hours: Optional[int] = Field(default=0, ge=0)
    independent_work_hours: Optional[int] = Field(default=0, ge=0)
    course_project_hours: Optional[int] = Field(default=0, ge=0)
    semester: Optional[int] = Field(default=1, ge=1, le=12)