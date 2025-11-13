from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.models.teacher import Teacher
from app.db.session import get_session

router = APIRouter()

@router.post("/teachers", tags=["Преподаватели"], summary="Создать преподавателя")
def create_teacher(teacher: Teacher, session: Session = Depends(get_session)):
    session.add(teacher)
    session.commit()
    session.refresh(teacher)
    return teacher

@router.get("/teachers", tags=["Преподаватели"], summary="Получить всех преподавателей")
def get_teachers(session: Session = Depends(get_session)):
    teachers = session.exec(select(Teacher)).all()
    if not teachers:
        raise HTTPException(status_code=404, detail="Преподаватели не найдены")
    return teachers

@router.get("/teachers/{id}", tags=["Преподаватели"], summary="Получить преподавателя по ID")
def get_teacher_by_id(id: int, session: Session = Depends(get_session)):
    teacher = session.get(Teacher, id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Преподаватель не найден")
    return teacher

@router.put("/teachers/{id}", tags=["Преподаватели"], summary="Обновить преподавателя")
def update_teacher(id: int, teacher: Teacher, session: Session = Depends(get_session)):
    db_teacher = session.get(Teacher, id)
    if not db_teacher:
        raise HTTPException(status_code=404, detail="Преподаватель не найден")
    db_teacher.first_name = teacher.first_name
    db_teacher.last_name = teacher.last_name
    db_teacher.patronymic = teacher.patronymic
    db_teacher.photo = teacher.photo
    session.commit()
    session.refresh(db_teacher)
    return db_teacher

@router.delete("/teachers/{id}", tags=["Преподаватели"], summary="Удалить преподавателя")
def delete_teacher(id: int, session: Session = Depends(get_session)):
    db_teacher = session.get(Teacher, id)
    if not db_teacher:
        raise HTTPException(status_code=404, detail="Преподаватель не найден")
    session.delete(db_teacher)
    session.commit()
    return {"message": "Преподаватель удален"}
