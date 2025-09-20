from sqlmodel import SQLModel, Field

class Specialty(SQLModel, table=True):
    __tablename__ = "specialties"
    
    specialty_code: str = Field(max_length=20, primary_key=True)
    specialty_name: str = Field(max_length=100)