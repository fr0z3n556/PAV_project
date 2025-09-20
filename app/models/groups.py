from sqlmodel import SQLModel, Field
from typing import Optional

class Groups(SQLModel, table=True):
    __tablename__ = "groups"
    
    group_number: str = Field(max_length=20, primary_key=True)
    specialty_code: Optional[str] = Field(foreign_key="specialties.specialty_code")
    education_form_id: Optional[int] = Field(foreign_key="education_form.education_form_id")
    group_type_id: Optional[int] = Field(foreign_key="group_type.group_type_id")