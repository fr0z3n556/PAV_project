from sqlmodel import Session, select
from app.models.teacher import Teacher
from fastapi import HTTPException

def create_teacher(teacher: Teacher, session: Session):
    session.add(teacher)
    session.commit()
    session.refresh(teacher)
    return teacher

def get_teachers(session: Session):
    teachers = session.exec(select(Teacher)).all()
    if not teachers:
        raise HTTPException(status_code=404, detail="Преподаватели не найдены")
    return teachers

def update_teacher(id: int, teacher: Teacher, session: Session):
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

def delete_teacher(id: int, session: Session):
    db_teacher = session.get(Teacher, id)
    if not db_teacher:
        raise HTTPException(status_code=404, detail="Преподаватель не найден")
    session.delete(db_teacher)
    session.commit()
    return {"message": "Преподаватель удален"}
