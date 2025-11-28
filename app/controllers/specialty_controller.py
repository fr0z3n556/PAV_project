from fastapi_pagination import Page
from fastapi import HTTPException
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.specialty import Specialty
from fastapi_pagination.ext.sqlalchemy import paginate

async def create_specialty(specialty: Specialty, session: AsyncSession):
    """
    Создает специальность в базе данных.

    Параметры:
    specialty (Specialty): Данные специальности для сохранения.
    session (AsyncSession): Сессия для работы с базой данных.

    Возвращаемое значение:
    Specialty: Возвращает созданную специальность после добавления.
    
    Исключения:
    HTTPException: Если возникает ошибка при добавлении специальности.
    """
    try:
        session.add(specialty)
        await session.commit()
        await session.refresh(specialty)
        return specialty
    except Exception as e:
        raise HTTPException(status_code=400, detail="Не удалось добавить специальность")

async def get_specialties(session: AsyncSession) -> Page[Specialty]:
    """
    Получает все специальности с пагинацией.

    Параметры:
    session (AsyncSession): Сессия для работы с базой данных.

    Возвращаемое значение:
    Page[Specialty]: Страница с данными всех специальностей.
    """
    return await paginate(session, select(Specialty))

async def get_specialty_by_id(id: int, session: AsyncSession):
    """
    Получает специальность по ID.

    Параметры:
    id (int): ID специальности.
    session (AsyncSession): Сессия для работы с базой данных.

    Возвращаемое значение:
    Specialty: Специальность с указанным ID.
    
    Исключения:
    HTTPException: Если специальность с таким ID не найдена.
    """
    specialty = await session.get(Specialty, id)
    if not specialty:
        raise HTTPException(status_code=404, detail="Специальность не найдена")
    return specialty

async def update_specialty(id: int, specialty: Specialty, session: AsyncSession):
    """
    Обновляет данные специальности по ID.

    Параметры:
    id (int): ID специальности.
    specialty (Specialty): Данные специальности для обновления.
    session (AsyncSession): Сессия для работы с базой данных.

    Возвращаемое значение:
    Specialty: Обновленная специальность.
    
    Исключения:
    HTTPException: Если специальность не найдена или ошибка при обновлении.
    """
    db_specialty = await session.get(Specialty, id)
    if not db_specialty:
        raise HTTPException(status_code=404, detail="Специальность не найдена")
    db_specialty.name = specialty.name
    db_specialty.code = specialty.code
    await session.commit()
    await session.refresh(db_specialty)
    return db_specialty

async def delete_specialty(id: int, session: AsyncSession):
    """
    Удаляет специальность по ID.

    Параметры:
    id (int): ID специальности.
    session (AsyncSession): Сессия для работы с базой данных.

    Возвращаемое значение:
    dict: Сообщение об удалении специальности.
    
    Исключения:
    HTTPException: Если специальность не найдена или ошибка при удалении.
    """
    db_specialty = await session.get(Specialty, id)
    if not db_specialty:
        raise HTTPException(status_code=404, detail="Специальность не найдена")
    session.delete(db_specialty)
    await session.commit()
    return {"message": "Специальность удалена"}

async def get_specialty_with_groups(id: int, session: AsyncSession):
    """
    Получает специальность со всеми её группами.

    Параметры:
    id (int): ID специальности.
    session (AsyncSession): Сессия для работы с базой данных.

    Возвращаемое значение:
    Specialty: Специальность с загруженными группами.
    
    Исключения:
    HTTPException: Если специальность не найдена.
    """
    result = await session.execute(
        select(Specialty)
        .where(Specialty.id == id)
        .options(selectinload(Specialty.groups))
    )
    specialty = result.scalar_one_or_none()
    if not specialty:
        raise HTTPException(status_code=404, detail="Специальность не найдена")
    return specialty
