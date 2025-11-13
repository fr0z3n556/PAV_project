from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.models.discipline import Discipline
from app.db.session import get_session

router = APIRouter()

@router.post("/disciplines", tags=["Дисциплины"], summary="Создать дисциплину")
def create_discipline(discipline: Discipline, session: Session = Depends(get_session)):
    try:
        session.add(discipline)
        session.commit()
        session.refresh(discipline)
        return discipline
    except Exception as e:
        raise HTTPException(status_code=400, detail="Не удалось добавить дисциплину")

@router.get("/disciplines", tags=["Дисциплины"], summary="Получить все дисциплины")
def get_disciplines(session: Session = Depends(get_session)):
    disciplines = session.exec(select(Discipline)).all()
    if not disciplines:
        raise HTTPException(status_code=404, detail="Дисциплины не найдены")
    return disciplines

@router.get("/disciplines/{id}", tags=["Дисциплины"], summary="Получить дисциплину по ID")
def get_discipline_by_id(id: int, session: Session = Depends(get_session)):
    discipline = session.get(Discipline, id)
    if not discipline:
        raise HTTPException(status_code=404, detail="Дисциплина не найдена")
    return discipline

@router.put("/disciplines/{id}", tags=["Дисциплины"], summary="Обновить дисциплину")
def update_discipline(id: int, discipline: Discipline, session: Session = Depends(get_session)):
    db_discipline = session.get(Discipline, id)
    if not db_discipline:
        raise HTTPException(status_code=404, detail="Дисциплина не найдена")
    db_discipline.name = discipline.name
    db_discipline.theoretical_hours = discipline.theoretical_hours
    db_discipline.practical_hours = discipline.practical_hours
    session.commit()
    session.refresh(db_discipline)
    return db_discipline

@router.delete("/disciplines/{id}", tags=["Дисциплины"], summary="Удалить дисциплину")
def delete_discipline(id: int, session: Session = Depends(get_session)):
    db_discipline = session.get(Discipline, id)
    if not db_discipline:
        raise HTTPException(status_code=404, detail="Дисциплина не найдена")
    session.delete(db_discipline)
    session.commit()
    return {"message": "Дисциплина удалена"}
