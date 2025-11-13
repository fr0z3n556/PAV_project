from sqlmodel import SQLModel, Field

class Specialty(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    code: str = Field(max_length=10)
    name: str = Field(max_length=255)
