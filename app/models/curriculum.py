from sqlmodel import SQLModel, Field, Relationship
from typing import Optional


class Curriculum(SQLModel, table=True):
    """
    Модель учебного плана - связывает специальность с дисциплинами.

    Параметры:
    id (int): Уникальный идентификатор записи учебного плана.
    specialty_id (int): ID специальности (ссылается на таблицу specialty).
    discipline_id (int): ID дисциплины (ссылается на таблицу discipline).
    semester (int): Семестр, в котором изучается дисциплина.
    hours_total (int): Общее количество часов дисциплины в учебном плане.
    """
    id: int = Field(default=None, primary_key=True)
    specialty_id: int = Field(foreign_key="specialty.id")  # Ссылается на таблицу specialty
    discipline_id: int = Field(foreign_key="discipline.id")  # Ссылается на таблицу discipline
    semester: int  # Семестр изучения
    hours_total: int  # Общее количество часов в учебном плане
    
    # Relationships
    specialty: Optional["Specialty"] = Relationship(back_populates="curriculums")
    discipline: Optional["Discipline"] = Relationship(back_populates="curriculums")
