from sqlmodel import Session, select
from app.models.curriculum import Curriculum
from app.models.specialty import Specialty
from app.models.discipline import Discipline
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import selectinload
from fastapi import HTTPException

async def create_curriculum(curriculum: Curriculum, session: Session):
    """
    Создание записи учебного плана.

    Параметры:
    curriculum (Curriculum): Объект учебного плана для создания.
    session (Session): Сессия базы данных.

    Возвращает:
    Curriculum: Созданный учебный план.
    """
    session.add(curriculum)
    await session.commit()
    await session.refresh(curriculum)
    return curriculum

async def get_curriculums(session: Session) -> Page[Curriculum]:
    """
    Получение всех записей учебного плана с пагинацией.

    Параметры:
    session (Session): Сессия базы данных.

    Возвращает:
    Page[Curriculum]: Список учебных планов с пагинацией.
    """
    return await paginate(session, select(Curriculum))

async def get_curriculum_by_id(curriculum_id: int, session: Session):
    """
    Получение записи учебного плана по ID.

    Параметры:
    curriculum_id (int): ID учебного плана.
    session (Session): Сессия базы данных.

    Возвращает:
    Curriculum: Найденный учебный план или None.
    """
    result = await session.execute(select(Curriculum).where(Curriculum.id == curriculum_id))
    return result.scalar_one_or_none()

async def update_curriculum(curriculum_id: int, curriculum_data: Curriculum, session: Session):
    """
    Обновление данных учебного плана.

    Параметры:
    curriculum_id (int): ID учебного плана для обновления.
    curriculum_data (Curriculum): Новые данные учебного плана.
    session (Session): Сессия базы данных.

    Возвращает:
    Curriculum: Обновленный учебный план или None.
    """
    curriculum = await get_curriculum_by_id(curriculum_id, session)
    if curriculum:
        curriculum.specialty_id = curriculum_data.specialty_id
        curriculum.discipline_id = curriculum_data.discipline_id
        curriculum.semester = curriculum_data.semester
        curriculum.hours_total = curriculum_data.hours_total
        await session.commit()
        await session.refresh(curriculum)
    return curriculum

async def delete_curriculum(curriculum_id: int, session: Session):
    """
    Удаление записи учебного плана.

    Параметры:
    curriculum_id (int): ID учебного плана для удаления.
    session (Session): Сессия базы данных.

    Возвращает:
    dict: Сообщение об успешном удалении или None.
    """
    curriculum = await get_curriculum_by_id(curriculum_id, session)
    if curriculum:
        await session.delete(curriculum)
        await session.commit()
        return {"message": "Учебный план успешно удален"}
    return None


async def get_full_curriculum_by_specialty(specialty_id: int, session: Session):
    """
    Получение полного учебного плана по специальности.

    Параметры:
    specialty_id (int): ID специальности.
    session (Session): Сессия базы данных.

    Возвращает:
    dict: Полный учебный план со структурой по семестрам.
    
    Исключения:
    HTTPException: Если специальность не найдена.
    """
    # Получаем специальность
    result = await session.execute(
        select(Specialty)
        .where(Specialty.id == specialty_id)
        .options(selectinload(Specialty.curriculums))
    )
    specialty = result.scalar_one_or_none()
    if not specialty:
        raise HTTPException(status_code=404, detail="Специальность не найдена")
    
    # Получаем все записи учебного плана с дисциплинами
    result = await session.execute(
        select(Curriculum)
        .where(Curriculum.specialty_id == specialty_id)
        .options(selectinload(Curriculum.discipline))
        .order_by(Curriculum.semester)
    )
    curriculums = result.scalars().all()
    
    # Строим структуру учебного плана
    semester_structure = {}
    total_hours = 0
    
    for item in curriculums:
        semester = item.semester
        if semester not in semester_structure:
            semester_structure[semester] = []
        
        semester_structure[semester].append({
            "discipline": item.discipline.name,
            "discipline_code": item.discipline.code,
            "hours": item.hours_total
        })
        total_hours += item.hours_total
    
    return {
        "specialty_id": specialty.id,
        "specialty_name": specialty.name,
        "specialty_code": specialty.code,
        "semesters": semester_structure,
        "total_hours": total_hours,
        "semester_count": len(semester_structure)
    }
