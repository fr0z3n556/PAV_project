from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from pydantic import EmailStr

class Teacher(SQLModel, table=True):
    __tablename__ = "teachers"
    
    teacher_id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str = Field(max_length=100)
    photo_path: Optional[str] = None
    
    # Relationships
    credentials: Optional["TeacherCredentials"] = Relationship(back_populates="teacher")
    workloads: List["TeacherWorkload"] = Relationship(back_populates="teacher")

class TeacherCredentials(SQLModel, table=True):
    __tablename__ = "teacher_credentials"
    
    teacher_id: int = Field(foreign_key="teachers.teacher_id", primary_key=True)
    username: str = Field(max_length=50, unique=True)
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    teacher: Teacher = Relationship(back_populates="credentials")

class Discipline(SQLModel, table=True):
    __tablename__ = "disciplines"
    
    discipline_code: str = Field(max_length=20, primary_key=True)
    discipline_name: str = Field(max_length=100)
    theory_hours: Optional[int] = Field(default=0, ge=0)
    practice_hours: Optional[int] = Field(default=0, ge=0)
    independent_work_hours: Optional[int] = Field(default=0, ge=0)
    course_project_hours: Optional[int] = Field(default=0, ge=0)
    semester: Optional[int] = Field(default=1, ge=1, le=12)
    
    # Relationships
    workloads: List["TeacherWorkload"] = Relationship(back_populates="discipline")

class Specialty(SQLModel, table=True):
    __tablename__ = "specialties"
    
    specialty_code: str = Field(max_length=20, primary_key=True)
    specialty_name: str = Field(max_length=100)
    
    # Relationships
    groups: List["Groups"] = Relationship(back_populates="specialty")

class EducationForm(SQLModel, table=True):
    __tablename__ = "education_form"
    
    education_form_id: Optional[int] = Field(default=None, primary_key=True)
    education_form_name: Optional[str] = Field(max_length=20)
    
    # Relationships
    groups: List["Groups"] = Relationship(back_populates="education_form")

class GroupType(SQLModel, table=True):
    __tablename__ = "group_type"
    
    group_type_id: Optional[int] = Field(default=None, primary_key=True)
    group_type_name: Optional[str] = Field(max_length=20)
    
    # Relationships
    groups: List["Groups"] = Relationship(back_populates="group_type")

class Groups(SQLModel, table=True):
    __tablename__ = "groups"
    
    group_number: str = Field(max_length=20, primary_key=True)
    specialty_code: Optional[str] = Field(foreign_key="specialties.specialty_code")
    education_form_id: Optional[int] = Field(foreign_key="education_form.education_form_id")
    group_type_id: Optional[int] = Field(foreign_key="group_type.group_type_id")
    
    # Relationships
    specialty: Optional[Specialty] = Relationship(back_populates="groups")
    education_form: Optional[EducationForm] = Relationship(back_populates="groups")
    group_type: Optional[GroupType] = Relationship(back_populates="groups")

class TeacherWorkload(SQLModel, table=True):
    __tablename__ = "teacher_workload"
    
    workload_id: Optional[int] = Field(default=None, primary_key=True)
    teacher_id: int = Field(foreign_key="teachers.teacher_id")
    discipline_code: str = Field(foreign_key="disciplines.discipline_code")
    semester: int = Field(ge=1, le=12)
    hours: int = Field(gt=0)
    
    # Relationships
    teacher: Teacher = Relationship(back_populates="workloads")
    discipline: Discipline = Relationship(back_populates="workloads")