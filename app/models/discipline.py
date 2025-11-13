from sqlmodel import SQLModel, Field

class Discipline(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    code: str = Field(max_length=10)
    name: str = Field(max_length=255)
    theoretical_hours: int
    practical_hours: int
    self_work_hours: int
    course_project_hours: int
    semester: int
