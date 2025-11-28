from fastapi_pagination import Page
from fastapi import HTTPException
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.group import Group
from fastapi_pagination.ext.sqlalchemy import paginate

async def create_group(group: Group, session: AsyncSession):
    """ 
    Создает группу в базе данных.
    
    Параметры:
    group (Group): Данные группы для сохранения.
    session (Session): Сессия для работы с базой данных.

    Возвращаемое значение:
    Group: Возвращает созданную группу после добавления.
    
    Исключения:
    HTTPException: Если возникает ошибка при добавлении группы.
    """
    session.add(group)
    await session.commit()
    await session.refresh(group)
    return group

async def get_groups(session: AsyncSession) -> Page[Group]:
    """Получает все группы с пагинацией."""
    return await paginate(session, select(Group))

async def get_group_by_id(id: int, session: AsyncSession):
    """ 
    Получает группу по ID.
    
    Параметры:
    id (int): ID группы.
    session (Session): Сессия для работы с базой данных.

    Возвращаемое значение:
    Group: Группа с указанным ID.
    
    Исключение:
    HTTPException: Если группа с таким ID не найдена.
    """
    group = await session.get(Group, id)
    if not group:
        raise HTTPException(status_code=404, detail="Группа не найдена")
    return group

async def update_group(id: int, group: Group, session: AsyncSession):
    """ 
    Обновляет данные группы по ID.
    
    Параметры:
    id (int): ID группы.
    group (Group): Данные группы для обновления.
    session (Session): Сессия для работы с базой данных.

    Возвращаемое значение:
    Group: Обновленная группа.
    
    Исключение:
    HTTPException: Если группа не найдена или ошибка при обновлении.
    """
    db_group = await session.get(Group, id)
    if not db_group:
        raise HTTPException(status_code=404, detail="Группа не найдена")
    db_group.group_number = group.group_number
    db_group.specialty_code = group.specialty_id
    db_group.form = group.form
    db_group.group_type = group.group_type
    await session.commit()
    await session.refresh(db_group)
    return db_group

async def delete_group(id: int, session: AsyncSession):
    """ 
    Удаляет группу по ID.
    
    Параметры:
    id (int): ID группы.
    session (Session): Сессия для работы с базой данных.

    Возвращаемое значение:
    dict: Сообщение об удалении группы.
    
    Исключение:
    HTTPException: Если группа не найдена или ошибка при удалении.
    """
    db_group = await session.get(Group, id)
    if not db_group:
        raise HTTPException(status_code=404, detail="Группа не найдена")
    session.delete(db_group)
    await session.commit()
    return {"message": "Группа удалена"}

async def get_group_with_specialty(id: int, session: AsyncSession):
    """
    Получает группу со специальностью.

    Параметры:
    id (int): ID группы.
    session (AsyncSession): Сессия для работы с базой данных.

    Возвращаемое значение:
    Group: Группа с загруженной специальностью.
    
    Исключение:
    HTTPException: Если группа не найдена.
    """
    result = await session.execute(
        select(Group)
        .where(Group.id == id)
        .options(selectinload(Group.specialty))
    )
    group = result.scalar_one_or_none()
    if not group:
        raise HTTPException(status_code=404, detail="Группа не найдена")
    return group
