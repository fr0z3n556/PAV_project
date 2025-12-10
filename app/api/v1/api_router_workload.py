from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.schemas.workload_schema import WorkloadSchema
from app.models.schemas.message_schema import MessageSchema
from app.db.session import get_session
from app.controllers.workload_controller import create_workload, get_workloads, get_workload_by_id, update_workload, delete_workload, get_workload_with_details, get_all_workloads_by_year, get_workloads_by_year_and_discipline
from app.core.auth import admin_required
from fastapi_pagination import Page

from app.models.workload import Workload

router = APIRouter()

@router.post("/workloads", tags=["Workloads"], summary="Создать нагрузку (Администратор)", response_model=WorkloadSchema)
async def create_workload_route(workload: Workload, session: AsyncSession = Depends(get_session), current_user: str = Depends(admin_required)):
    """
    Создает нагрузку с помощью контроллера.
    
    Параметры:
    workload (Workload): Данные для создания нагрузки.
    session (AsyncSession): Сессия для работы с базой данных.
    current_user (str): Пользователь, выполняющий запрос, проверяется на роль администратора.
    
    Возвращаемое значение:
    WorkloadSchema: Созданная нагрузка.
    """
    return await create_workload(workload, session)

@router.get("/workloads", tags=["Workloads"], summary="Получить все нагрузки с пагинацией (Администратор)", response_model=Page[WorkloadSchema])
async def get_workloads_route(session: AsyncSession = Depends(get_session), admin: str = Depends(admin_required)):
    """
    Получает все нагрузки с пагинацией.
    
    ТОЛЬКО ДЛЯ АДМИНИСТРАТОРА.
    
    Параметры:
    session (AsyncSession): Сессия для работы с базой данных.
    
    Возвращаемое значение:
    Page[WorkloadSchema]: Пагинированный список всех нагрузок.
    """
    return await get_workloads(session)

@router.get("/workloads/{id}", tags=["Workloads"], summary="Получить нагрузку по ID (Администратор)", response_model=WorkloadSchema)
async def get_workload_by_id_route(id: int, session: AsyncSession = Depends(get_session), admin: str = Depends(admin_required)):
    """
    Получает нагрузку по ID через контроллер.
    
    ТОЛЬКО ДЛЯ АДМИНИСТРАТОРА.
    
    Параметры:
    id (int): ID нагрузки.
    session (AsyncSession): Сессия для работы с базой данных.
    
    Возвращаемое значение:
    WorkloadSchema: Нагрузка по ID.
    """
    return await get_workload_by_id(id, session)

@router.put("/workloads/{id}", tags=["Workloads"], summary="Обновить нагрузку (Администратор)", response_model=WorkloadSchema)
async def update_workload_route(id: int, workload: Workload, session: AsyncSession = Depends(get_session), current_user: str = Depends(admin_required)):
    """
    Обновляет нагрузку по ID с помощью контроллера.
    
    Параметры:
    id (int): ID нагрузки.
    workload (Workload): Новые данные для нагрузки.
    session (AsyncSession): Сессия для работы с базой данных.
    current_user (str): Пользователь, выполняющий запрос, проверяется на роль администратора.
    
    Возвращаемое значение:
    WorkloadSchema: Обновленная нагрузка.
    """
    return await update_workload(id, workload, session)

@router.delete("/workloads/{id}", tags=["Workloads"], summary="Удалить нагрузку (Администратор)", response_model=MessageSchema)
async def delete_workload_route(id: int, session: AsyncSession = Depends(get_session), current_user: str = Depends(admin_required)):
    """
    Удаляет нагрузку по ID через контроллер.
    
    Параметры:
    id (int): ID нагрузки.
    session (AsyncSession): Сессия для работы с базой данных.
    current_user (str): Пользователь, выполняющий запрос, проверяется на роль администратора.
    
    Возвращаемое значение:
    dict: Сообщение об успешном удалении.
    """
    return await delete_workload(id, session)

@router.get("/workloads/{id}/details", tags=["Workloads"], summary="Получить нагрузку с деталями (Администратор)", response_model=Workload)
async def get_workload_with_details_route(id: int, session: AsyncSession = Depends(get_session), admin: str = Depends(admin_required)):
    """
    Получает нагрузку с преподавателем и дисциплиной.
    
    ТОЛЬКО ДЛЯ АДМИНИСТРАТОРА.
    
    Параметры:
    id (int): ID нагрузки.
    session (AsyncSession): Сессия для работы с базой данных.
    
    Возвращаемое значение:
    Workload: Нагрузка с загруженными преподавателем и дисциплиной.
    """
    return await get_workload_with_details(id, session)

@router.get("/workloads/year/{year}", tags=["Workloads"], summary="Нагрузка всех преподавателей за год (Администратор)")
async def get_all_workloads_by_year_route(year: int, session: AsyncSession = Depends(get_session), admin: str = Depends(admin_required)):
    """
    Получает нагрузку всех преподавателей за учебный год.
    
    ТОЛЬКО ДЛЯ АДМИНИСТРАТОРА.
    
    Параметры:
    year (int): Год (например, 2024).
    session (AsyncSession): Сессия для работы с базой данных.
    
    Возвращаемое значение:
    list[Workload]: Список всех нагрузок с преподавателями и дисциплинами.
    """
    return await get_all_workloads_by_year(year, session)

@router.get("/workloads/by-year-discipline", tags=["Workloads"], summary="Найти преподавателя по году и предмету (Администратор)")
async def get_workloads_by_year_and_discipline_route(year: int, discipline_id: int, session: AsyncSession = Depends(get_session), admin: str = Depends(admin_required)):
    """
    Находит какой преподаватель ведет дисциплину в указанном году.
    
    ТОЛЬКО ДЛЯ АДМИНИСТРАТОРА.
    
    Параметры:
    year (int): Год.
    discipline_id (int): ID дисциплины.
    session (AsyncSession): Сессия для работы с базой данных.
    
    Возвращаемое значение:
    list[Workload]: Список нагрузок с преподавателями и часами.
    """
    return await get_workloads_by_year_and_discipline(year, discipline_id, session)
