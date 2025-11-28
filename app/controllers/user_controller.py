from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession  # ← ВАЖНО!
from sqlmodel import select
from app.core.auth import create_access_token
from app.db.session import get_session  # ← должен возвращать AsyncSession
from app.models.schemas.userSchema import UserSchema, UserRegisterSchema
from app.models.user import Users
from app.models.teacher import Teacher
import os

SECRET_KEY = os.getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
ALGORITHM = os.getenv("ALGORITHM")


async def login(
    form_data: UserSchema = Depends(UserSchema.as_form),
    session: AsyncSession = Depends(get_session),  # ← AsyncSession
):
    # ⚠️ execute — асинхронный, scalars() — для извлечения ORM-объектов
    result = await session.execute(
        select(Users).where(Users.username == form_data.username)
    )
    user = result.scalars().one_or_none()

    if not user or form_data.password != user.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль",
        )

    access_token = await create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}  # ← БЕЗ await!


async def register_user(
    user_data: UserRegisterSchema,
    session: AsyncSession,
):
    """
    Регистрация нового пользователя (только для админа).
    
    Параметры:
    user_data (UserRegisterSchema): Данные нового пользователя.
    session (AsyncSession): Сессия для работы с базой данных.
    
    Возвращаемое значение:
    dict: Сообщение об успешной регистрации.
    
    Исключения:
    HTTPException: Если логин уже существует, преподаватель не найден, или не указан teacher_id для role=user.
    """
    # 1. Проверяем что логин уникален
    result = await session.execute(
        select(Users).where(Users.username == user_data.username)
    )
    existing_user = result.scalars().one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Пользователь с логином '{user_data.username}' уже существует"
        )
    
    # 2. Если роль = user, проверяем что teacher_id указан и существует
    if user_data.role == "user":
        if not user_data.teacher_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Для роли 'user' обязательно указать teacher_id"
            )
        # Проверяем существование преподавателя
        teacher = await session.get(Teacher, user_data.teacher_id)
        if not teacher:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Преподаватель с ID {user_data.teacher_id} не найден"
            )
    
    # 3. Если роль = admin, teacher_id должен быть None
    if user_data.role == "admin":
        user_data.teacher_id = None
    
    # 4. Создаем нового пользователя
    new_user = Users(
        username=user_data.username,
        password=user_data.password,  # TODO: хешировать пароль!
        role=user_data.role,
        teacher_id=user_data.teacher_id
    )
    
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    
    return {
        "message": "Пользователь успешно зарегистрирован",
        "user_id": new_user.id,
        "username": new_user.username,
        "role": new_user.role,
        "teacher_id": new_user.teacher_id
    }