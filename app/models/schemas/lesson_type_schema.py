from pydantic import BaseModel, ConfigDict

class LessonTypeSchema(BaseModel):
    """
    Схема для валидации типа занятия.

    Параметры:
    name (str): Название типа занятия (лекция, практика, лабораторная).
    """
    name: str  # Название типа занятия

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Лекция"
            }
        }
    )
