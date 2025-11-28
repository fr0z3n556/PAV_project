from fastapi_pagination import Page
from fastapi import HTTPException
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.teacher import Teacher
from fastapi_pagination.ext.sqlalchemy import paginate

async def create_teacher(teacher: Teacher, session: AsyncSession):
    """ 
    Создает преподавателя в базе данных.
    
    Параметры:
    teacher (Teacher): Данные преподавателя для сохранения.
    session (Session): Сессия для работы с базой данных.

    Возвращаемое значение:
    Teacher: Возвращает созданного преподавателя после добавления.
    
    Исключения:
    HTTPException: Если возникает ошибка при добавлении преподавателя.
    """
    try:
        session.add(teacher)
        await session.commit()
        await session.refresh(teacher)
        return teacher
    except Exception as e:
        raise HTTPException(status_code=400, detail="Не удалось добавить преподавателя")

async def get_teachers(session: AsyncSession) -> Page[Teacher]:
    """Получает всех преподавателей с пагинацией."""
    return await paginate(session, select(Teacher))

async def get_teacher_by_id(id: int, session: AsyncSession):
    """ 
    Получает преподавателя по ID.
    
    Параметры:
    id (int): ID преподавателя.
    session (Session): Сессия для работы с базой данных.

    Возвращаемое значение:
    Teacher: Преподаватель с указанным ID.
    
    Исключение:
    HTTPException: Если преподаватель с таким ID не найден.
    """
    teacher = await session.get(Teacher, id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Преподаватель не найден")
    return teacher

async def update_teacher(id: int, teacher: Teacher, session: AsyncSession):
    """ 
    Обновляет данные преподавателя по ID.
    
    Параметры:
    id (int): ID преподавателя.
    teacher (Teacher): Данные преподавателя для обновления.
    session (Session): Сессия для работы с базой данных.

    Возвращаемое значение:
    Teacher: Обновленный преподаватель.
    
    Исключение:
    HTTPException: Если преподаватель не найден или ошибка при обновлении.
    """
    db_teacher = await session.get(Teacher, id)
    if not db_teacher:
        raise HTTPException(status_code=404, detail="Преподаватель не найден")
    db_teacher.first_name = teacher.first_name
    db_teacher.last_name = teacher.last_name
    db_teacher.patronymic = teacher.patronymic
    db_teacher.photo = teacher.photo
    await session.commit()
    await session.refresh(db_teacher)
    return db_teacher

async def delete_teacher(id: int, session: AsyncSession):
    """ 
    Удаляет преподавателя по ID.
    
    Параметры:
    id (int): ID преподавателя.
    session (Session): Сессия для работы с базой данных.

    Возвращаемое значение:
    dict: Сообщение об удалении преподавателя.
    
    Исключение:
    HTTPException: Если преподаватель не найден или ошибка при удалении.
    """
    db_teacher = await session.get(Teacher, id)
    if not db_teacher:
        raise HTTPException(status_code=404, detail="Преподаватель не найден")
    session.delete(db_teacher)
    await session.commit()
    return {"message": "Преподаватель удален"}

async def get_teacher_with_workloads(id: int, session: AsyncSession):
    """
    Получает преподавателя со всеми его нагрузками.

    Параметры:
    id (int): ID преподавателя.
    session (AsyncSession): Сессия для работы с базой данных.

    Возвращаемое значение:
    Teacher: Преподаватель с загруженными нагрузками.
    
    Исключение:
    HTTPException: Если преподаватель не найден.
    """
    result = await session.execute(
        select(Teacher)
        .where(Teacher.id == id)
        .options(selectinload(Teacher.workloads))
    )
    teacher = result.scalar_one_or_none()
    if not teacher:
        raise HTTPException(status_code=404, detail="Преподаватель не найден")
    return teacher
