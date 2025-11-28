from pydantic import BaseModel, ConfigDict

class GroupSchema(BaseModel):
    """
    Схема для валидации данных группы.

    Параметры:
    group_number (str): Номер группы.
    specialty_id (int): ID специальности (внешний ключ).
    form (str): Форма обучения.
    group_type (str): Тип группы.
    """
    group_number: str  # Номер группы
    specialty_id: int  # ID специальности
    form: str  # Форма обучения
    group_type: str  # Тип группы

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "group_number": "ИП-31",
                "specialty_id": 1,
                "form": "Очная",
                "group_type": "Бюджет"
            }
        }
    )
