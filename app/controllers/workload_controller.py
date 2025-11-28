from fastapi_pagination import Page
from fastapi import HTTPException
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.workload import Workload
from app.models.teacher import Teacher
from fastapi_pagination.ext.sqlalchemy import paginate

async def create_workload(workload: Workload, session: AsyncSession):
    """ 
    Создает нагрузку в базе данных.
    
    Параметры:
    workload (Workload): Данные нагрузки для сохранения.
    session (Session): Сессия для работы с базой данных.

    Возвращаемое значение:
    Workload: Возвращает созданную нагрузку после добавления.
    
    Исключения:
    HTTPException: Если возникает ошибка при добавлении нагрузки.
    """
    try:
        session.add(workload)
        await session.commit()
        await session.refresh(workload)
        return workload
    except Exception as e:
        raise HTTPException(status_code=400, detail="Не удалось добавить нагрузку")

async def get_workloads(session: AsyncSession) -> Page[Workload]:
    """Получает все нагрузки с пагинацией."""
    return await paginate(session, select(Workload))

async def get_workload_by_id(id: int, session: AsyncSession):
    """ 
    Получает нагрузку по ID.
    
    Параметры:
    id (int): ID нагрузки.
    session (Session): Сессия для работы с базой данных.

    Возвращаемое значение:
    Workload: Нагрузка с указанным ID.
    
    Исключение:
    HTTPException: Если нагрузка с таким ID не найдена.
    """
    workload = await session.get(Workload, id)
    if not workload:
        raise HTTPException(status_code=404, detail="Нагрузка не найдена")
    return workload

async def update_workload(id: int, workload: Workload, session: AsyncSession):
    """ 
    Обновляет данные нагрузки по ID.
    
    Параметры:
    id (int): ID нагрузки.
    workload (Workload): Данные нагрузки для обновления.
    session (Session): Сессия для работы с базой данных.

    Возвращаемое значение:
    Workload: Обновленная нагрузка.
    
    Исключение:
    HTTPException: Если нагрузка не найдена или ошибка при обновлении.
    """
    db_workload = await session.get(Workload, id)
    if not db_workload:
        raise HTTPException(status_code=404, detail="Нагрузка не найдена")
    db_workload.teacher_id = workload.teacher_id
    db_workload.discipline_id = workload.discipline_id
    db_workload.hours = workload.hours
    db_workload.semester = workload.semester
    await session.commit()
    await session.refresh(db_workload)
    return db_workload

async def delete_workload(id: int, session: AsyncSession):
    """ 
    Удаляет нагрузку по ID.
    
    Параметры:
    id (int): ID нагрузки.
    session (Session): Сессия для работы с базой данных.

    Возвращаемое значение:
    dict: Сообщение об удалении нагрузки.
    
    Исключение:
    HTTPException: Если нагрузка не найдена или ошибка при удалении.
    """
    db_workload = await session.get(Workload, id)
    if not db_workload:
        raise HTTPException(status_code=404, detail="Нагрузка не найдена")
    session.delete(db_workload)
    await session.commit()
    return {"message": "Нагрузка удалена"}

async def get_workload_with_details(id: int, session: AsyncSession):
    """
    Получает нагрузку с преподавателем и дисциплиной.

    Параметры:
    id (int): ID нагрузки.
    session (AsyncSession): Сессия для работы с базой данных.

    Возвращаемое значение:
    Workload: Нагрузка с загруженными преподавателем и дисциплиной.
    
    Исключение:
    HTTPException: Если нагрузка не найдена.
    """
    result = await session.execute(
        select(Workload)
        .where(Workload.id == id)
        .options(selectinload(Workload.teacher), selectinload(Workload.discipline))
    )
    workload = result.scalar_one_or_none()
    if not workload:
        raise HTTPException(status_code=404, detail="Нагрузка не найдена")
    return workload

async def get_all_workloads_by_year(year: int, session: AsyncSession):
    """
    Получает нагрузку всех преподавателей за учебный год.

    Параметры:
    year (int): Год (например, 2024 для 2024-2025 учебного года).
    session (AsyncSession): Сессия для работы с базой данных.

    Возвращаемое значение:
    list[Workload]: Список нагрузок с преподавателями и дисциплинами.
    """
    result = await session.execute(
        select(Workload)
        .where(Workload.year == year)
        .options(selectinload(Workload.teacher), selectinload(Workload.discipline))
        .order_by(Workload.teacher_id, Workload.semester)
    )
    return result.scalars().all()

async def get_workloads_by_year_and_discipline(year: int, discipline_id: int, session: AsyncSession):
    """
    Получает нагрузку по году и дисциплине.

    Параметры:
    year (int): Год.
    discipline_id (int): ID дисциплины.
    session (AsyncSession): Сессия для работы с базой данных.

    Возвращаемое значение:
    list[Workload]: Список нагрузок с преподавателями.
    """
    result = await session.execute(
        select(Workload)
        .where(Workload.year == year, Workload.discipline_id == discipline_id)
        .options(selectinload(Workload.teacher), selectinload(Workload.discipline))
        .order_by(Workload.teacher_id)
    )
    return result.scalars().all()

async def get_teacher_workloads_by_year(teacher_id: int, year: int, session: AsyncSession):
    """
    Получает нагрузку конкретного преподавателя за год.

    Параметры:
    teacher_id (int): ID преподавателя.
    year (int): Год.
    session (AsyncSession): Сессия для работы с базой данных.

    Возвращаемое значение:
    list[Workload]: Список нагрузок преподавателя с дисциплинами.
    
    Исключение:
    HTTPException: Если преподаватель не найден.
    """
    # Проверяем существование преподавателя
    teacher = await session.get(Teacher, teacher_id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Преподаватель не найден")
    
    result = await session.execute(
        select(Workload)
        .where(Workload.teacher_id == teacher_id, Workload.year == year)
        .options(selectinload(Workload.discipline))
        .order_by(Workload.semester)
    )
    return result.scalars().all()
