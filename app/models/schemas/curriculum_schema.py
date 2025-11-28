from pydantic import BaseModel, ConfigDict

class CurriculumSchema(BaseModel):
    """
    Схема для валидации данных учебного плана.

    Параметры:
    specialty_id (int): ID специальности.
    discipline_id (int): ID дисциплины.
    semester (int): Семестр изучения.
    hours_total (int): Общее количество часов.
    """
    specialty_id: int  # ID специальности
    discipline_id: int  # ID дисциплины
    semester: int  # Семестр
    hours_total: int  # Общее количество часов

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "specialty_id": 1,
                "discipline_id": 1,
                "semester": 1,
                "hours_total": 120
            }
        }
    )
