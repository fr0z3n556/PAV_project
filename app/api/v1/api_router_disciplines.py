from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.discipline import Discipline
from app.models.schemas.discipline_schema import DisciplineSchema
from app.models.schemas.message_schema import MessageSchema
from app.db.session import get_session
from app.controllers.discipline_controller import create_discipline, get_disciplines, get_discipline_by_id, update_discipline, delete_discipline
from app.core.auth import admin_required
from fastapi_pagination import Page

router = APIRouter()

@router.post("/disciplines", tags=["Disciplines"], summary="Создать дисциплину (Администратор)", response_model=DisciplineSchema)
async def create_discipline_route(discipline: Discipline, session: AsyncSession = Depends(get_session), current_user: str = Depends(admin_required)):
    """
    Создает дисциплину с помощью контроллера.
    
    Параметры:
    discipline (Discipline): Данные для создания дисциплины.
    session (AsyncSession): Сессия для работы с базой данных.
    current_user (str): Пользователь, выполняющий запрос, проверяется на роль администратора.
    
    Возвращаемое значение:
    DisciplineSchema: Созданная дисциплина.
    """
    return await create_discipline(discipline, session)

@router.get("/disciplines", tags=["Disciplines"], summary="Получить все дисциплины с пагинацией (Все пользователи)", response_model=Page[DisciplineSchema])
async def get_disciplines_route(session: AsyncSession = Depends(get_session)):
    """
    Получает все дисциплины с пагинацией.

    Параметры:
    session (AsyncSession): Сессия для работы с базой данных.

    Возвращаемое значение:
    Page[DisciplineSchema]: Пагинированный список всех дисциплин.
    """
    return await get_disciplines(session)

@router.get("/disciplines/{id}", tags=["Disciplines"], summary="Получить дисциплину по ID (Все пользователи)", response_model=DisciplineSchema)
async def get_discipline_by_id_route(id: int, session: AsyncSession = Depends(get_session)):
    """
    Получает дисциплину по ID через контроллер.
    
    Параметры:
    id (int): ID дисциплины.
    session (AsyncSession): Сессия для работы с базой данных.

    Возвращаемое значение:
    DisciplineSchema: Дисциплина по ID.
    """
    return await get_discipline_by_id(id, session)

@router.put("/disciplines/{id}", tags=["Disciplines"], summary="Обновить дисциплину (Администратор)", response_model=DisciplineSchema)
async def update_discipline_route(id: int, discipline: Discipline, session: AsyncSession = Depends(get_session), current_user: str = Depends(admin_required)):
    """
    Обновляет дисциплину по ID с помощью контроллера.
    
    Параметры:
    id (int): ID дисциплины.
    discipline (Discipline): Новые данные для дисциплины.
    session (AsyncSession): Сессия для работы с базой данных.
    current_user (str): Пользователь, выполняющий запрос, проверяется на роль администратора.
    
    Возвращаемое значение:
    DisciplineSchema: Обновленная дисциплина.
    """
    return await update_discipline(id, discipline, session)

@router.delete("/disciplines/{id}", tags=["Disciplines"], summary="Удалить дисциплину (Администратор)", response_model=MessageSchema)
async def delete_discipline_route(id: int, session: AsyncSession = Depends(get_session), current_user: str = Depends(admin_required)):
    """
    Удаляет дисциплину по ID через контроллер.
    
    Параметры:
    id (int): ID дисциплины.
    session (AsyncSession): Сессия для работы с базой данных.
    current_user (str): Пользователь, выполняющий запрос, проверяется на роль администратора.
    
    Возвращаемое значение:
    dict: Сообщение об успешном удалении.
    """
    return await delete_discipline(id, session)
