from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.schemas.group_schema import GroupSchema
from app.models.schemas.message_schema import MessageSchema
from app.models.group import Group
from app.db.session import get_session
from app.controllers.group_controller import create_group, get_groups, get_group_by_id, update_group, delete_group, get_group_with_specialty
from app.core.auth import admin_required
from fastapi_pagination import Page

router = APIRouter()

@router.post("/groups", tags=["Groups"], summary="Создать группу (Администратор)", response_model=GroupSchema)
async def create_group_route(group: Group, session: AsyncSession = Depends(get_session), current_user: str = Depends(admin_required)):
    """
    Создает группу с помощью контроллера.
    
    Параметры:
    group (Group): Данные для создания группы.
    session (AsyncSession): Сессия для работы с базой данных.
    current_user (str): Пользователь, выполняющий запрос, проверяется на роль администратора.
    
    Возвращаемое значение:
    GroupSchema: Созданная группа.
    """
    return await create_group(group, session)

@router.get("/groups", tags=["Groups"], summary="Получить все группы с пагинацией (Все пользователи)", response_model=Page[GroupSchema])
async def get_groups_route(session: AsyncSession = Depends(get_session)):
    """
    Получает все группы с пагинацией.

    Параметры:
    session (AsyncSession): Сессия для работы с базой данных.

    Возвращаемое значение:
    Page[GroupSchema]: Пагинированный список всех групп.
    """
    return await get_groups(session)

@router.get("/groups/{id}", tags=["Groups"], summary="Получить группу по ID (Все пользователи)", response_model=GroupSchema)
async def get_group_by_id_route(id: int, session: AsyncSession = Depends(get_session)):
    """
    Получает группу по ID через контроллер.
    
    Параметры:
    id (int): ID группы.
    session (AsyncSession): Сессия для работы с базой данных.

    Возвращаемое значение:
    GroupSchema: Группа по ID.
    """
    return await get_group_by_id(id, session)

@router.put("/groups/{id}", tags=["Groups"], summary="Обновить группу (Администратор)", response_model=GroupSchema)
async def update_group_route(id: int, group: Group, session: AsyncSession = Depends(get_session), current_user: str = Depends(admin_required)):
    """
    Обновляет группу по ID с помощью контроллера.
    
    Параметры:
    id (int): ID группы.
    group (Group): Новые данные для группы.
    session (AsyncSession): Сессия для работы с базой данных.
    current_user (str): Пользователь, выполняющий запрос, проверяется на роль администратора.
    
    Возвращаемое значение:
    GroupSchema: Обновленная группа.
    """
    return await update_group(id, group, session)

@router.delete("/groups/{id}", tags=["Groups"], summary="Удалить группу (Администратор)", response_model=MessageSchema)
async def delete_group_route(id: int, session: AsyncSession = Depends(get_session), current_user: str = Depends(admin_required)):
    """
    Удаляет группу по ID через контроллер.
    
    Параметры:
    id (int): ID группы.
    session (AsyncSession): Сессия для работы с базой данных.
    current_user (str): Пользователь, выполняющий запрос, проверяется на роль администратора.
    
    Возвращаемое значение:
    dict: Сообщение об успешном удалении.
    """
    return await delete_group(id, session)

@router.get("/groups/{id}/with-specialty", tags=["Groups"], summary="Получить группу со специальностью (Все пользователи)", response_model=Group)
async def get_group_with_specialty_route(id: int, session: AsyncSession = Depends(get_session)):
    """
    Получает группу со специальностью.
    
    Параметры:
    id (int): ID группы.
    session (AsyncSession): Сессия для работы с базой данных.
    
    Возвращаемое значение:
    Group: Группа с загруженной специальностью.
    """
    return await get_group_with_specialty(id, session)
