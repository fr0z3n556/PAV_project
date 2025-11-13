from sqlmodel import Session, select
from app.models.workload import Workload
from fastapi import HTTPException

def create_workload(workload: Workload, session: Session):
    session.add(workload)
    session.commit()
    session.refresh(workload)
    return workload

def get_workload(session: Session):
    workloads = session.exec(select(Workload)).all()
    if not workloads:
        raise HTTPException(status_code=404, detail="Нагрузка не найдена")
    return workloads

def delete_workload(id: int, session: Session):
    db_workload = session.get(Workload, id)
    if not db_workload:
        raise HTTPException(status_code=404, detail="Нагрузка не найдена")
    session.delete(db_workload)
    session.commit()
    return {"message": "Нагрузка удалена"}


