from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.schemas.teacher_schema import TeacherSchema
from app.models.schemas.message_schema import MessageSchema
from app.db.session import get_session
from app.controllers.teacher_controller import create_teacher, get_teachers, get_teacher_by_id, update_teacher, delete_teacher, get_teacher_with_workloads
from app.controllers.workload_controller import get_teacher_workloads_by_year
from app.core.auth import admin_required, get_current_user
from app.models.user import Users
from fastapi_pagination import Page

from app.models.teacher import Teacher

router = APIRouter()

@router.post("/teachers", tags=["Teachers"], summary="Создать преподавателя (Администратор)", response_model=TeacherSchema)
async def create_teacher_route(teacher: Teacher, session: AsyncSession = Depends(get_session), current_user: str = Depends(admin_required)):
    """
    Создает преподавателя с помощью контроллера.
    
    Параметры:
    teacher (Teacher): Данные для создания преподавателя.
    session (AsyncSession): Сессия для работы с базой данных.
    current_user (str): Пользователь, выполняющий запрос, проверяется на роль администратора.
    
    Возвращаемое значение:
    TeacherSchema: Созданный преподаватель.
    """
    return await create_teacher(teacher, session)

@router.get("/teachers", tags=["Teachers"], summary="Получить всех преподавателей с пагинацией (Администратор)", response_model=Page[TeacherSchema])
async def get_teachers_route(session: AsyncSession = Depends(get_session), admin: str = Depends(admin_required)):
    """
    Получает всех преподавателей с пагинацией.
    
    ТОЛЬКО ДЛЯ АДМИНИСТРАТОРА.
    
    Параметры:
    session (AsyncSession): Сессия для работы с базой данных.
    
    Возвращаемое значение:
    Page[TeacherSchema]: Пагинированный список всех преподавателей.
    """
    return await get_teachers(session)

@router.get("/teachers/{id}", tags=["Teachers"], summary="Получить преподавателя по ID (Администратор)", response_model=TeacherSchema)
async def get_teacher_by_id_route(id: int, session: AsyncSession = Depends(get_session), admin: str = Depends(admin_required)):
    """
    Получает преподавателя по ID через контроллер.
    
    ТОЛЬКО ДЛЯ АДМИНИСТРАТОРА.
    
    Параметры:
    id (int): ID преподавателя.
    session (AsyncSession): Сессия для работы с базой данных.
    
    Возвращаемое значение:
    TeacherSchema: Преподаватель по ID.
    """
    return await get_teacher_by_id(id, session)

@router.put("/teachers/{id}", tags=["Teachers"], summary="Обновить преподавателя (Администратор)", response_model=TeacherSchema)
async def update_teacher_route(id: int, teacher: Teacher, session: AsyncSession = Depends(get_session), current_user: str = Depends(admin_required)):
    """
    Обновляет преподавателя по ID с помощью контроллера.
    
    Параметры:
    id (int): ID преподавателя.
    teacher (Teacher): Новые данные для преподавателя.
    session (AsyncSession): Сессия для работы с базой данных.
    current_user (str): Пользователь, выполняющий запрос, проверяется на роль администратора.
    
    Возвращаемое значение:
    TeacherSchema: Обновленный преподаватель.
    """
    return await update_teacher(id, teacher, session)

@router.delete("/teachers/{id}", tags=["Teachers"], summary="Удалить преподавателя (Администратор)", response_model=MessageSchema)
async def delete_teacher_route(id: int, session: AsyncSession = Depends(get_session), current_user: str = Depends(admin_required)):
    """
    Удаляет преподавателя по ID через контроллер.
    
    Параметры:
    id (int): ID преподавателя.
    session (AsyncSession): Сессия для работы с базой данных.
    current_user (str): Пользователь, выполняющий запрос, проверяется на роль администратора.
    
    Возвращаемое значение:
    dict: Сообщение об успешном удалении.
    """
    return await delete_teacher(id, session)

@router.get("/teachers/{id}/workloads", tags=["Teachers"], summary="Получить преподавателя с нагрузками (Преподаватель, Администратор)", response_model=Teacher)
async def get_teacher_with_workloads_route(
    id: int,
    session: AsyncSession = Depends(get_session),
    current_user: Users = Depends(get_current_user)
):
    """
    Получает преподавателя со всеми его нагрузками.
    
    Преподаватель (role=user) может видеть только свою нагрузку.
    Администратор может видеть любую нагрузку.
    
    Параметры:
    id (int): ID преподавателя.
    session (AsyncSession): Сессия для работы с базой данных.
    
    Возвращаемое значение:
    Teacher: Преподаватель с загруженными нагрузками.
    """
    # Если обычный user - проверяем что он смотрит только свою нагрузку
    print(f"DEBUG: User role={current_user.role}, teacher_id={current_user.teacher_id}, requested id={id}")
    if current_user.role == "user":
        if current_user.teacher_id != id:
            raise HTTPException(
                status_code=403,
                detail="Вы можете просматривать только свою нагрузку"
            )
    return await get_teacher_with_workloads(id, session)

@router.get("/teachers/{id}/workloads/year/{year}", tags=["Teachers"], summary="Нагрузка преподавателя за год (Преподаватель, Администратор)")
async def get_teacher_workloads_by_year_route(
    id: int,
    year: int,
    session: AsyncSession = Depends(get_session),
    current_user: Users = Depends(get_current_user)
):
    """
    Получает нагрузку конкретного преподавателя за год.
    
    Преподаватель (role=user) может видеть только свою нагрузку.
    Администратор может видеть любую нагрузку.
    
    Параметры:
    id (int): ID преподавателя.
    year (int): Год.
    session (AsyncSession): Сессия для работы с базой данных.
    
    Возвращаемое значение:
    list[Workload]: Список нагрузок с дисциплинами.
    """
    # Если обычный user - проверяем что он смотрит только свою нагрузку
    print(f"DEBUG: User role={current_user.role}, teacher_id={current_user.teacher_id}, requested id={id}")
    if current_user.role == "user":
        if current_user.teacher_id != id:
            raise HTTPException(
                status_code=403,
                detail="Вы можете просматривать только свою нагрузку"
            )
    return await get_teacher_workloads_by_year(id, year, session)
