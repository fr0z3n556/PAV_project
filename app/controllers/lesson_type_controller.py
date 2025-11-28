from sqlmodel import Session, select
from app.models.lesson_type import LessonType
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

async def create_lesson_type(lesson_type: LessonType, session: Session):
    """
    Создание типа занятия.

    Параметры:
    lesson_type (LessonType): Объект типа занятия для создания.
    session (Session): Сессия базы данных.

    Возвращает:
    LessonType: Созданный тип занятия.
    """
    session.add(lesson_type)
    await session.commit()
    await session.refresh(lesson_type)
    return lesson_type

async def get_lesson_types(session: Session) -> Page[LessonType]:
    """
    Получение всех типов занятий с пагинацией.

    Параметры:
    session (Session): Сессия базы данных.

    Возвращает:
    Page[LessonType]: Список типов занятий с пагинацией.
    """
    return await paginate(session, select(LessonType))

async def get_lesson_type_by_id(lesson_type_id: int, session: Session):
    """
    Получение типа занятия по ID.

    Параметры:
    lesson_type_id (int): ID типа занятия.
    session (Session): Сессия базы данных.

    Возвращает:
    LessonType: Найденный тип занятия или None.
    """
    result = await session.execute(select(LessonType).where(LessonType.id == lesson_type_id))
    return result.scalar_one_or_none()

async def update_lesson_type(lesson_type_id: int, lesson_type_data: LessonType, session: Session):
    """
    Обновление типа занятия.

    Параметры:
    lesson_type_id (int): ID типа занятия для обновления.
    lesson_type_data (LessonType): Новые данные типа занятия.
    session (Session): Сессия базы данных.

    Возвращает:
    LessonType: Обновленный тип занятия или None.
    """
    lesson_type = await get_lesson_type_by_id(lesson_type_id, session)
    if lesson_type:
        lesson_type.name = lesson_type_data.name
        await session.commit()
        await session.refresh(lesson_type)
    return lesson_type

async def delete_lesson_type(lesson_type_id: int, session: Session):
    """
    Удаление типа занятия.

    Параметры:
    lesson_type_id (int): ID типа занятия для удаления.
    session (Session): Сессия базы данных.

    Возвращает:
    dict: Сообщение об успешном удалении или None.
    """
    lesson_type = await get_lesson_type_by_id(lesson_type_id, session)
    if lesson_type:
        await session.delete(lesson_type)
        await session.commit()
        return {"message": "Тип занятия успешно удален"}
    return None
