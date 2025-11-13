from sqlmodel import Session, select
from app.models.discipline import Discipline
from fastapi import HTTPException

def create_discipline(discipline: Discipline, session: Session):
    session.add(discipline)
    session.commit()
    session.refresh(discipline)
    return discipline

def get_disciplines(session: Session):
    disciplines = session.exec(select(Discipline)).all()
    if not disciplines:
        raise HTTPException(status_code=404, detail="Дисциплины не найдены")
    return disciplines

def update_discipline(id: int, discipline: Discipline, session: Session):
    db_discipline = session.get(Discipline, id)
    if not db_discipline:
        raise HTTPException(status_code=404, detail="Дисциплина не найдена")
    db_discipline.name = discipline.name
    db_discipline.theoretical_hours = discipline.theoretical_hours
    db_discipline.practical_hours = discipline.practical_hours
    db_discipline.self_work_hours = discipline.self_work_hours
    db_discipline.course_project_hours = discipline.course_project_hours
    db_discipline.semester = discipline.semester
    session.commit()
    session.refresh(db_discipline)
    return db_discipline

def delete_discipline(id: int, session: Session):
    db_discipline = session.get(Discipline, id)
    if not db_discipline:
        raise HTTPException(status_code=404, detail="Дисциплина не найдена")
    session.delete(db_discipline)
    session.commit()
    return {"message": "Дисциплина удалена"}
