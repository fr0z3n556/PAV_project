from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.models.specialty import Specialty
from app.db.session import get_session

router = APIRouter()

@router.post("/specialties", tags=["Специальности"], summary="Создать специальность")
def create_specialty(specialty: Specialty, session: Session = Depends(get_session)):
    try:
        session.add(specialty)
        session.commit()
        session.refresh(specialty)
        return specialty
    except Exception as e:
        raise HTTPException(status_code=400, detail="Не удалось добавить специальность")

@router.get("/specialties", tags=["Специальности"], summary="Получить все специальности")
def get_specialties(session: Session = Depends(get_session)):
    specialties = session.exec(select(Specialty)).all()
    if not specialties:
        raise HTTPException(status_code=404, detail="Специальности не найдены")
    return specialties

@router.get("/specialties/{id}", tags=["Специальности"], summary="Получить специальность по ID")
def get_specialty_by_id(id: int, session: Session = Depends(get_session)):
    specialty = session.get(Specialty, id)
    if not specialty:
        raise HTTPException(status_code=404, detail="Специальность не найдена")
    return specialty

@router.put("/specialties/{id}", tags=["Специальности"], summary="Обновить специальность")
def update_specialty(id: int, specialty: Specialty, session: Session = Depends(get_session)):
    db_specialty = session.get(Specialty, id)
    if not db_specialty:
        raise HTTPException(status_code=404, detail="Специальность не найдена")
    db_specialty.name = specialty.name
    db_specialty.code = specialty.code
    session.commit()
    session.refresh(db_specialty)
    return db_specialty

@router.delete("/specialties/{id}", tags=["Специальности"], summary="Удалить специальность")
def delete_specialty(id: int, session: Session = Depends(get_session)):
    db_specialty = session.get(Specialty, id)
    if not db_specialty:
        raise HTTPException(status_code=404, detail="Специальность не найдена")
    session.delete(db_specialty)
    session.commit()
    return {"message": "Специальность удалена"}
