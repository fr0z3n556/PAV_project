from fastapi_pagination import Page
from fastapi import HTTPException
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.discipline import Discipline
from fastapi_pagination.ext.sqlalchemy import paginate

async def create_discipline(discipline: Discipline, session: AsyncSession):
    """ 
    Создает дисциплину в базе данных.
    
    Параметры:
    discipline (Discipline): Данные дисциплины для сохранения.
    session (Session): Сессия для работы с базой данных.

    Возвращаемое значение:
    Discipline: Возвращает созданную дисциплину после добавления.
    
    Исключения:
    HTTPException: Если возникает ошибка при добавлении дисциплины.
    """
    try:
        session.add(discipline)
        await session.commit()
        await session.refresh(discipline)
        return discipline
    except Exception as e:
        raise HTTPException(status_code=400, detail="Не удалось добавить дисциплину")

async def get_disciplines(session: AsyncSession) -> Page[Discipline]:
    """Получает все дисциплины с пагинацией."""
    return await paginate(session, select(Discipline))

async def get_discipline_by_id(id: int, session: AsyncSession):
    """ 
    Получает дисциплину по ID.
    
    Параметры:
    id (int): ID дисциплины.
    session (Session): Сессия для работы с базой данных.

    Возвращаемое значение:
    Discipline: Дисциплина с указанным ID.
    
    Исключение:
    HTTPException: Если дисциплина с таким ID не найдена.
    """
    discipline = await session.get(Discipline, id)
    if not discipline:
        raise HTTPException(status_code=404, detail="Дисциплина не найдена")
    return discipline

async def update_discipline(id: int, discipline: Discipline, session: AsyncSession):
    """ 
    Обновляет данные дисциплины по ID.
    
    Параметры:
    id (int): ID дисциплины.
    discipline (Discipline): Данные дисциплины для обновления.
    session (Session): Сессия для работы с базой данных.

    Возвращаемое значение:
    Discipline: Обновленная дисциплина.
    
    Исключение:
    HTTPException: Если дисциплина не найдена или ошибка при обновлении.
    """
    db_discipline = await session.get(Discipline, id)
    if not db_discipline:
        raise HTTPException(status_code=404, detail="Дисциплина не найдена")
    db_discipline.name = discipline.name
    db_discipline.code = discipline.code
    db_discipline.theoretical_hours = discipline.theoretical_hours
    db_discipline.practical_hours = discipline.practical_hours
    db_discipline.self_work_hours = discipline.self_work_hours
    db_discipline.course_project_hours = discipline.course_project_hours
    db_discipline.semester = discipline.semester
    await session.commit()
    await session.refresh(db_discipline)
    return db_discipline

async def delete_discipline(id: int, session: AsyncSession):
    """ 
    Удаляет дисциплину по ID.
    
    Параметры:
    id (int): ID дисциплины.
    session (Session): Сессия для работы с базой данных.

    Возвращаемое значение:
    dict: Сообщение об удалении дисциплины.
    
    Исключение:
    HTTPException: Если дисциплина не найдена или ошибка при удалении.
    """
    db_discipline = await session.get(Discipline, id)
    if not db_discipline:
        raise HTTPException(status_code=404, detail="Дисциплина не найдена")
    session.delete(db_discipline)
    await session.commit()
    return {"message": "Дисциплина удалена"}
