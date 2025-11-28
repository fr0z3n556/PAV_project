from sqlmodel import SQLModel, Field
from typing import Optional

class Users(SQLModel,table=True):
    """
    Модель пользователя.
    
    Параметры:
    id (int): Уникальный идентификатор пользователя.
    username (str): Логин пользователя.
    password (str): Хешированный пароль.
    role (str): Роль пользователя (user или admin), по умолчанию user.
    teacher_id (Optional[int]): ID преподавателя (только для role=user, для admin=None).
    """
    id: int = Field(primary_key=True, default=None, sa_column_kwargs={"autoincrement": True})
    username: str = Field(unique=True, index=True)
    password: str = Field()
    role: str = Field(default="user")  # По умолчанию обычный user
    teacher_id: Optional[int] = Field(default=None, foreign_key="teacher.id")  # Связь с преподавателем