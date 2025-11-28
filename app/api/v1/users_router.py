from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import Session
from app.controllers.specialty_controller import create_specialty, get_specialties, get_specialty_by_id, update_specialty, delete_specialty
from app.controllers.user_controller import login, register_user
from app.db.session import get_session
from app.models.schemas.specialty_schema import SpecialtySchema
from app.models.schemas.userSchema import UserSchema, UserRegisterSchema
from app.core.auth import admin_required
from app.models.user import Users

router = APIRouter(prefix='/users')

@router.post("/token", tags=["users"], response_model=None)
async def add_login(form_data: UserSchema=Depends(UserSchema.as_form), session: Session = Depends(get_session)):
    return await login(form_data, session)

@router.post("/register", tags=["users"], summary="Регистрация нового пользователя")
async def register_user_route(
    user_data: UserRegisterSchema,
    session: AsyncSession = Depends(get_session),
    admin: Users = Depends(admin_required)
):
    """
    Регистрация нового пользователя (только для администратора).
    
    Параметры:
    - username (str): Логин нового пользователя
    - password (str): Пароль
    - role (str): Роль - 'user' или 'admin' (по умолчанию 'user')
    - teacher_id (int, optional): ID преподавателя (обязательно для role='user')
    
    Возвращает:
    - Сообщение об успешной регистрации
    """
    return await register_user(user_data, session)