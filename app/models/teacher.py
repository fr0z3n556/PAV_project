from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class Teacher(SQLModel, table=True):
    """
    Модель преподавателя.

    Параметры:
    id (int): Уникальный идентификатор преподавателя.
    first_name (str): Имя преподавателя.
    last_name (str): Фамилия преподавателя.
    patronymic (str): Отчество преподавателя.
    photo (str): Фото преподавателя.
    """
    id: int = Field(default=None, primary_key=True)
    first_name: str = Field(max_length=255)  # Имя преподавателя
    last_name: str = Field(max_length=255)  # Фамилия преподавателя
    patronymic: str = Field(max_length=255)  # Отчество преподавателя
    photo: str = Field(max_length=255)  # Фото преподавателя
    
    # Relationship: один преподаватель -> много нагрузок
    workloads: List["Workload"] = Relationship(back_populates="teacher")
