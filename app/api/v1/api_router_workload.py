from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.models.workload import Workload
from app.db.session import get_session

router = APIRouter()

# Создание нагрузки
@router.post("/workload", tags=["Нагрузка"], summary="Создать нагрузку")
def create_workload(workload: Workload, session: Session = Depends(get_session)):
    session.add(workload)
    session.commit()
    session.refresh(workload)
    return workload

@router.get("/workload", tags=["Нагрузка"], summary="Получить нагрузку")
def get_workload(session: Session = Depends(get_session)):
    workloads = session.exec(select(Workload)).all()
    if not workloads:
        raise HTTPException(status_code=404, detail="Нагрузка не найдена")
    return workloads

@router.get("/workload/{id}", tags=["Нагрузка"], summary="Получить нагрузку по ID")
def get_workload_by_id(id: int, session: Session = Depends(get_session)):
    workload = session.get(Workload, id)
    if not workload:
        raise HTTPException(status_code=404, detail="Нагрузка не найдена")
    return workload

# Удаление нагрузки
@router.delete("/workload/{id}", tags=["Нагрузка"], summary="Удалить нагрузку")
def delete_workload(id: int, session: Session = Depends(get_session)):
    db_workload = session.get(Workload, id)
    if not db_workload:
        raise HTTPException(status_code=404, detail="Нагрузка не найдена")
    session.delete(db_workload)
    session.commit()
    return {"message": "Нагрузка удалена"}

# Обновление нагрузки
@router.put("/workload/{id}", tags=["Нагрузка"], summary="Обновить нагрузку")
def update_workload(id: int, workload: Workload, session: Session = Depends(get_session)):
    # Получаем существующую нагрузку по ID
    db_workload = session.get(Workload, id)
    
    if not db_workload:
        raise HTTPException(status_code=404, detail="Нагрузка не найдена")

    # Обновляем данные
    db_workload.teacher_id = workload.teacher_id
    db_workload.discipline_id = workload.discipline_id
    db_workload.hours = workload.hours
    db_workload.semester = workload.semester

    try:
        session.commit()
        session.refresh(db_workload)
        return db_workload
    except Exception as e:
        raise HTTPException(status_code=500, detail="Ошибка при обновлении нагрузки")
