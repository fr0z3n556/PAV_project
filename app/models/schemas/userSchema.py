from pydantic import BaseModel, Field, field_validator
from fastapi import Form
from typing import Optional

class UserSchema(BaseModel):
    """
    Схема для авторизации (логин).
    """
    username: str
    password: str

    @classmethod
    async def as_form(
        cls,
        username: str = Form(..., description="Имя пользователя"),
        password: str = Form(..., description="Пароль"),
    ):
        return cls(username=username, password=password)

class UserRegisterSchema(BaseModel):
    """
    Схема для регистрации нового пользователя (только для админа).
    
    Параметры:
    username (str): Логин нового пользователя.
    password (str): Пароль.
    role (str): Роль - 'user' или 'admin', по умолчанию 'user'.
    teacher_id (Optional[int]): ID преподавателя (обязателен для role='user', для 'admin' не нужен).
    """
    username: str
    password: str
    role: str = Field(default="user", pattern="^(user|admin)$")  # Только user или admin
    teacher_id: Optional[int] = None
    
    @field_validator('role')
    @classmethod
    def validate_role(cls, v):
        """
        Проверяет что роль только 'user' или 'admin'.
        """
        if v not in ["user", "admin"]:
            raise ValueError("Роль должна быть 'user' или 'admin'")
        return v.lower()  # Приводим к нижнему регистру