from sqlmodel import SQLModel, Field
from typing import Optional

class EducationForm(SQLModel, table=True):
    __tablename__ = "education_form"
    
    education_form_id: Optional[int] = Field(default=None, primary_key=True)
    education_form_name: Optional[str] = Field(max_length=20)