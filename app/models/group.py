from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

class Group(SQLModel, table=True):
    """
    Модель для группы.

    Параметры:
    id (int): Уникальный идентификатор группы.
    group_number (str): Номер группы.
    specialty_id (int): ID специальности (внешний ключ).
    form (str): Форма обучения (очно/заочно).
    group_type (str): Тип группы (бюджет/внебюджет).
    """
    __tablename__ = "groups"  # Явное имя таблицы, избегаем зарезервированное слово "group"
    
    id: int = Field(default=None, primary_key=True)
    group_number: str = Field(max_length=20, unique=True, index=True)
    specialty_id: int = Field(foreign_key="specialty.id")  # Foreign key к специальности
    form: str = Field(max_length=10)  # очно / заочно
    group_type: str = Field(max_length=20)  # бюджет / внебюджет
    
    # Relationship: группа -> одна специальность
    specialty: Optional["Specialty"] = Relationship(back_populates="groups")
