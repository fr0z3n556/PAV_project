from sqlmodel import Session, select
from app.models.specialty import Specialty
from fastapi import HTTPException

def create_specialty(specialty: Specialty, session: Session):
    try:
        session.add(specialty)
        session.commit()
        session.refresh(specialty)
        return specialty
    except Exception as e:
        raise HTTPException(status_code=400, detail="Не удалось добавить специальность")

def get_specialties(session: Session):
    specialties = session.exec(select(Specialty)).all()
    if not specialties:
        raise HTTPException(status_code=404, detail="Специальности не найдены")
    return specialties

def update_specialty(id: int, specialty: Specialty, session: Session):
    db_specialty = session.get(Specialty, id)
    if not db_specialty:
        raise HTTPException(status_code=404, detail="Специальность не найдена")
    db_specialty.name = specialty.name
    db_specialty.code = specialty.code
    session.commit()
    session.refresh(db_specialty)
    return db_specialty

def delete_specialty(id: int, session: Session):
    db_specialty = session.get(Specialty, id)
    if not db_specialty:
        raise HTTPException(status_code=404, detail="Специальность не найдена")
    session.delete(db_specialty)
    session.commit()
    return {"message": "Специальность удалена"}
