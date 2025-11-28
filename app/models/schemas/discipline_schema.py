from pydantic import BaseModel, ConfigDict

class DisciplineSchema(BaseModel):
    """
    Схема для валидации дисциплины.

    Параметры:
    code (str): Код дисциплины.
    name (str): Название дисциплины.
    theoretical_hours (int): Часы теоретического обучения.
    practical_hours (int): Часы практического обучения.
    self_work_hours (int): Часы самостоятельной работы.
    course_project_hours (int): Часы на курсовую работу.
    semester (int): Семестр, в котором преподается дисциплина.
    """
    code: str  # Код дисциплины
    name: str  # Название дисциплины
    theoretical_hours: int  # Часы теоретического обучения
    practical_hours: int  # Часы практического обучения
    self_work_hours: int  # Часы самостоятельной работы
    course_project_hours: int  # Часы на курсовую работу
    semester: int  # Семестр

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "code": "Математика",
                "name": "Математика для ИТ",
                "theoretical_hours": 40,
                "practical_hours": 20,
                "self_work_hours": 30,
                "course_project_hours": 50,
                "semester": 2
            }
        }
    )
