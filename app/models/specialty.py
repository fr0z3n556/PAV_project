from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List


class Specialty(SQLModel, table=True):
    """
    Модель для специальности.

    Параметры:
    id (int): Уникальный идентификатор специальности.
    code (str): Код специальности.
    name (str): Название специальности.
    """
    id: int = Field(default=None, primary_key=True)
    code: str = Field(max_length=10, unique=True, index=True)
    name: str = Field(max_length=255)
    
    # Relationship: одна специальность -> много групп
    groups: List["Group"] = Relationship(back_populates="specialty")
    
    # Relationship: одна специальность -> много записей учебного плана
    curriculums: List["Curriculum"] = Relationship(back_populates="specialty")
