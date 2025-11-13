from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.models.group import Group
from app.db.session import get_session

router = APIRouter()

@router.post("/groups", tags=["Группы"], summary="Создать группу")
def create_group(group: Group, session: Session = Depends(get_session)):
    session.add(group)
    session.commit()
    session.refresh(group)
    return group

@router.get("/groups", tags=["Группы"], summary="Получить все группы")
def get_groups(session: Session = Depends(get_session)):
    groups = session.exec(select(Group)).all()
    if not groups:
        raise HTTPException(status_code=404, detail="Группы не найдены")
    return groups

@router.get("/groups/{id}", tags=["Группы"], summary="Получить группу по ID")
def get_group_by_id(id: int, session: Session = Depends(get_session)):
    group = session.get(Group, id)
    if not group:
        raise HTTPException(status_code=404, detail="Группа не найдена")
    return group

@router.put("/groups/{id}", tags=["Группы"], summary="Обновить группу")
def update_group(id: int, group: Group, session: Session = Depends(get_session)):
    db_group = session.get(Group, id)
    if not db_group:
        raise HTTPException(status_code=404, detail="Группа не найдена")
    db_group.group_number = group.group_number
    db_group.specialty_code = group.specialty_code
    db_group.form = group.form
    db_group.group_type = group.group_type
    session.commit()
    session.refresh(db_group)
    return db_group

@router.delete("/groups/{id}", tags=["Группы"], summary="Удалить группу")
def delete_group(id: int, session: Session = Depends(get_session)):
    db_group = session.get(Group, id)
    if not db_group:
        raise HTTPException(status_code=404, detail="Группа не найдена")
    session.delete(db_group)
    session.commit()
    return {"message": "Группа удалена"}
