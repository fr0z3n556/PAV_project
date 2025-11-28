from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.schemas.specialty_schema import SpecialtySchema
from app.db.session import get_session
from app.controllers.specialty_controller import create_specialty, get_specialties, get_specialty_by_id, update_specialty, delete_specialty, get_specialty_with_groups
from app.core.auth import admin_required
from fastapi_pagination import Page

from app.models.specialty import Specialty

router = APIRouter()

@router.post("/specialties", tags=["Specialties"], summary="Создать специальность", response_model=SpecialtySchema)
async def create_specialty_route(specialty: Specialty, session: AsyncSession = Depends(get_session), current_user: str = Depends(admin_required)):
    """
    Создает специальность с помощью контроллера.
    
    Параметры:
    specialty (Specialty): Данные для создания специальности.
    session (AsyncSession): Сессия для работы с базой данных.
    current_user (str): Пользователь, выполняющий запрос, проверяется на роль администратора.
    
    Возвращаемое значение:
    SpecialtySchema: Созданная специальность.
    """
    return await create_specialty(specialty, session)

@router.get("/specialties", tags=["Specialties"], summary="Получить все специальности с пагинацией", response_model=Page[SpecialtySchema])
async def get_specialties_route(session: AsyncSession = Depends(get_session)):
    """
    Получает все специальности с пагинацией.

    Параметры:
    session (AsyncSession): Сессия для работы с базой данных.

    Возвращаемое значение:
    Page[SpecialtySchema]: Пагинированный список всех специальностей.
    """
    return await get_specialties(session)

@router.get("/specialties/{id}", tags=["Specialties"], summary="Получить специальность по ID", response_model=SpecialtySchema)
async def get_specialty_by_id_route(id: int, session: AsyncSession = Depends(get_session)):
    """
    Получает специальность по ID через контроллер.
    
    Параметры:
    id (int): ID специальности.
    session (AsyncSession): Сессия для работы с базой данных.

    Возвращаемое значение:
    SpecialtySchema: Специальность по ID.
    """
    return await get_specialty_by_id(id, session)

@router.put("/specialties/{id}", tags=["Specialties"], summary="Обновить специальность", response_model=SpecialtySchema)
async def update_specialty_route(id: int, specialty: Specialty, session: AsyncSession = Depends(get_session), current_user: str = Depends(admin_required)):
    """
    Обновляет специальность по ID с помощью контроллера.
    
    Параметры:
    id (int): ID специальности.
    specialty (Specialty): Новые данные для специальности.
    session (AsyncSession): Сессия для работы с базой данных.
    current_user (str): Пользователь, выполняющий запрос, проверяется на роль администратора.
    
    Возвращаемое значение:
    SpecialtySchema: Обновленная специальность.
    """
    return await update_specialty(id, specialty, session)

@router.delete("/specialties/{id}", tags=["Specialties"], summary="Удалить специальность", response_model=SpecialtySchema)
async def delete_specialty_route(id: int, session: AsyncSession = Depends(get_session), current_user: str = Depends(admin_required)):
    """
    Удаляет специальность по ID через контроллер.
    
    Параметры:
    id (int): ID специальности.
    session (AsyncSession): Сессия для работы с базой данных.
    current_user (str): Пользователь, выполняющий запрос, проверяется на роль администратора.
    
    Возвращаемое значение:
    dict: Сообщение об успешном удалении.
    """
    return await delete_specialty(id, session)

@router.get("/specialties/{id}/groups", tags=["Specialties"], summary="Получить специальность с группами", response_model=Specialty)
async def get_specialty_with_groups_route(id: int, session: AsyncSession = Depends(get_session)):
    """
    Получает специальность со всеми её группами.
    
    Параметры:
    id (int): ID специальности.
    session (AsyncSession): Сессия для работы с базой данных.
    
    Возвращаемое значение:
    Specialty: Специальность с загруженными группами.
    """
    return await get_specialty_with_groups(id, session)
