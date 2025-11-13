from sqlmodel import SQLModel, Field

class Workload(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    teacher_id: int = Field(foreign_key="teacher.id")
    discipline_id: int = Field(foreign_key="discipline.id")
    hours: int
    semester: int
