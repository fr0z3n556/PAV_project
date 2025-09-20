from sqlmodel import SQLModel, Field
from typing import Optional

class TeacherWorkload(SQLModel, table=True):
    __tablename__ = "teacher_workload"
    
    workload_id: Optional[int] = Field(default=None, primary_key=True)
    teacher_id: int = Field(foreign_key="teachers.teacher_id")
    discipline_code: str = Field(foreign_key="disciplines.discipline_code")
    semester: int = Field(ge=1, le=12)
    hours: int = Field(gt=0)