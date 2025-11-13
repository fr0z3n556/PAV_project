from sqlmodel import SQLModel, Field

class Teacher(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    first_name: str = Field(max_length=255)
    last_name: str = Field(max_length=255)
    patronymic: str = Field(max_length=255)
    photo: str = Field(max_length=255)
