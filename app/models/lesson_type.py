from sqlmodel import SQLModel, Field, Relationship
from typing import List

class LessonType(SQLModel, table=True):
    """
    Модель типа занятия (микро-табличка).

    Параметры:
    id (int): Уникальный идентификатор типа занятия.
    name (str): Название типа занятия (лекция, практика, лабораторная).
    """
    id: int = Field(default=None, primary_key=True)
    name: str = Field(max_length=50, unique=True)  # Название типа: лекция, практика, лабораторная работа
