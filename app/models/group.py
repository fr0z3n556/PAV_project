from sqlmodel import SQLModel, Field

class Group(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    group_number: str = Field(max_length=20)
    specialty_code: str = Field(max_length=10)
    form: str = Field(max_length=10)
    group_type: str = Field(max_length=10)
