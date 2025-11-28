from pydantic import BaseModel, ConfigDict
from sqlmodel import Field

class SpecialtySchema(BaseModel):
    """
    Схема для валидации данных специальности.

    Параметры:
    code (str): Код специальности.
    name (str): Название специальности.
    """
    code: str  # Код специальности
    name: str  # Название специальности

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "code": "ИП",
                "name": "Информационные системы и программирование",
            }
        }
    )
