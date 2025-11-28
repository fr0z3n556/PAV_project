from pydantic import BaseModel, ConfigDict

class WorkloadSchema(BaseModel):
    """
    Схема для валидации нагрузки.

    Параметры:
    teacher_id (int): ID преподавателя.
    discipline_id (int): ID дисциплины.
    hours (int): Количество часов.
    semester (int): Семестр.
    year (int): Учебный год.
    """
    teacher_id: int  # ID преподавателя
    discipline_id: int  # ID дисциплины
    hours: int  # Количество часов
    semester: int  # Семестр
    year: int  # Учебный год

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "teacher_id": 1,
                "discipline_id": 2,
                "hours": 40,
                "semester": 2,
                "year": 2024
            }
        }
    )
