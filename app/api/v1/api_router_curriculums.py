from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.db.session import get_session
from app.models.curriculum import Curriculum
from app.models.schemas.curriculum_schema import CurriculumSchema
from app.models.schemas.message_schema import MessageSchema
from app.controllers.curriculum_controller import create_curriculum,get_curriculums,get_curriculum_by_id,update_curriculum,delete_curriculum,get_full_curriculum_by_specialty
from fastapi_pagination import Page
from app.core.auth import admin_required

router = APIRouter(prefix="/curriculums", tags=["Curriculums"])

@router.post("", response_model=Curriculum, summary="Создать учебный план (Администратор)")
async def create_curriculum_route(curriculum: CurriculumSchema,session: Session = Depends(get_session),current_user = Depends(admin_required)):
    """
    Создать новую запись учебного плана.
    """
    curriculum_obj = Curriculum(**curriculum.model_dump())
    return await create_curriculum(curriculum_obj, session)

@router.get("", response_model=Page[Curriculum], summary="Получить все учебные планы (Администратор)")
async def get_curriculums_route(session: Session = Depends(get_session),current_user = Depends(admin_required)):
    """
    Получить все записи учебного плана с пагинацией.
    """
    return await get_curriculums(session)

@router.get("/{curriculum_id}", response_model=Curriculum, summary="Получить учебный план по ID (Администратор)")
async def get_curriculum_route(curriculum_id: int,session: Session = Depends(get_session),current_user = Depends(admin_required)):
    """
    Получить учебный план по ID.
    """
    curriculum = await get_curriculum_by_id(curriculum_id, session)
    if not curriculum:
        raise HTTPException(status_code=404, detail="Учебный план не найден")
    return curriculum

@router.put("/{curriculum_id}", response_model=Curriculum, summary="Обновить учебный план (Администратор)")
async def update_curriculum_route(curriculum_id: int,curriculum: CurriculumSchema,session: Session = Depends(get_session),current_user = Depends(admin_required)):
    """
    Обновить данные учебного плана по ID.
    """
    curriculum_obj = Curriculum(**curriculum.model_dump())
    updated_curriculum = await update_curriculum(curriculum_id, curriculum_obj, session)
    if not updated_curriculum:
        raise HTTPException(status_code=404, detail="Учебный план не найден")
    return updated_curriculum

@router.delete("/{curriculum_id}", summary="Удалить учебный план (Администратор)", response_model=MessageSchema)
async def delete_curriculum_route(curriculum_id: int,session: Session = Depends(get_session),current_user = Depends(admin_required)):
    """
    Удалить учебный план по ID.
    """
    result = await delete_curriculum(curriculum_id, session)
    if not result:
        raise HTTPException(status_code=404, detail="Учебный план не найден")
    return result

@router.get("/full-plan/specialty/{specialty_id}", summary="Получить полный учебный план по специальности (Администратор)")
async def get_full_curriculum_by_specialty_route(
    specialty_id: int,
    session: Session = Depends(get_session),
    current_user = Depends(admin_required)
):
    """
    Получить полный учебный план по специальности со структурой по семестрам.
    
    Возвращает:
    - specialty_id: ID специальности
    - specialty_name: Название специальности
    - specialty_code: Код специальности
    - semesters: Структура учебного плана по семестрам
    - total_hours: Общее количество часов
    - semester_count: Количество семестров
    """
    return await get_full_curriculum_by_specialty(specialty_id, session)
