from pydantic import BaseModel, ConfigDict

class TeacherSchema(BaseModel):
    """
    Схема для валидации данных преподавателя.

    Параметры:
    first_name (str): Имя преподавателя.
    last_name (str): Фамилия преподавателя.
    patronymic (str): Отчество преподавателя.
    photo (str): Фото преподавателя.
    """
    first_name: str  # Имя преподавателя
    last_name: str  # Фамилия преподавателя
    patronymic: str  # Отчество преподавателя
    photo: str = None  # Фото преподавателя (опционально)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "first_name": "Андрей",
                "last_name": "Пашухин",
                "patronymic": "Викторович",
                "photo": "/photo.jpg"
            }
        }
    )
