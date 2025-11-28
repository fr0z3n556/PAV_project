from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

class Workload(SQLModel, table=True):
    """
    Модель для нагрузки преподавателя.

    Параметры:
    id (int): Уникальный идентификатор нагрузки.
    teacher_id (int): ID преподавателя (ссылается на таблицу teacher).
    discipline_id (int): ID дисциплины (ссылается на таблицу discipline).
    hours (int): Количество часов.
    semester (int): Семестр, для которого назначена нагрузка.
    year (int): Учебный год (например, 2024 для 2024-2025).
    """
    id: int = Field(default=None, primary_key=True)
    teacher_id: int = Field(foreign_key="teacher.id")  # Ссылается на таблицу teacher
    discipline_id: int = Field(foreign_key="discipline.id")  # Ссылается на таблицу discipline
    hours: int  # Количество часов
    semester: int  # Семестр
    year: int  # Учебный год
    
    # Relationships
    teacher: Optional["Teacher"] = Relationship(back_populates="workloads")
    discipline: Optional["Discipline"] = Relationship(back_populates="workloads")
