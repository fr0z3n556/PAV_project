from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.db.session import get_session
from app.models.lesson_type import LessonType
from app.models.schemas.lesson_type_schema import LessonTypeSchema
from app.models.schemas.message_schema import MessageSchema
from app.controllers.lesson_type_controller import create_lesson_type,get_lesson_types,get_lesson_type_by_id,update_lesson_type,delete_lesson_type

from fastapi_pagination import Page
from app.core.auth import admin_required

router = APIRouter(prefix="/lesson-types",tags=["Lesson Types"])

@router.post("", response_model=LessonType, summary="Создать тип занятия (Администратор)")
async def create_lesson_type_route(lesson_type: LessonTypeSchema,session: Session = Depends(get_session),current_user = Depends(admin_required)):
    """
    Создать новый тип занятия.
    """
    lesson_type_obj = LessonType(**lesson_type.model_dump())
    return await create_lesson_type(lesson_type_obj, session)

@router.get("", response_model=Page[LessonType], summary="Получить все типы занятий (Администратор)")
async def get_lesson_types_route(session: Session = Depends(get_session),current_user = Depends(admin_required)):
    """
    Получить все типы занятий с пагинацией.
    """
    return await get_lesson_types(session)

@router.get("/{lesson_type_id}", response_model=LessonType, summary="Получить тип занятия по ID (Администратор)")
async def get_lesson_type_route(lesson_type_id: int,session: Session = Depends(get_session),current_user = Depends(admin_required)):
    """
    Получить тип занятия по ID.
    """
    lesson_type = await get_lesson_type_by_id(lesson_type_id, session)
    if not lesson_type:
        raise HTTPException(status_code=404, detail="Тип занятия не найден")
    return lesson_type

@router.put("/{lesson_type_id}", response_model=LessonType, summary="Обновить тип занятия (Администратор)")
async def update_lesson_type_route(lesson_type_id: int,lesson_type: LessonTypeSchema,session: Session = Depends(get_session),current_user = Depends(admin_required)):
    """
    Обновить тип занятия по ID.
    """
    lesson_type_obj = LessonType(**lesson_type.model_dump())
    updated_lesson_type = await update_lesson_type(lesson_type_id, lesson_type_obj, session)
    if not updated_lesson_type:
        raise HTTPException(status_code=404, detail="Тип занятия не найден")
    return updated_lesson_type

@router.delete("/{lesson_type_id}", summary="Удалить тип занятия (Администратор)", response_model=MessageSchema)
async def delete_lesson_type_route(lesson_type_id: int,session: Session = Depends(get_session),current_user = Depends(admin_required)):
    """
    Удалить тип занятия по ID.
    """
    result = await delete_lesson_type(lesson_type_id, session)
    if not result:
        raise HTTPException(status_code=404, detail="Тип занятия не найден")
    return result
