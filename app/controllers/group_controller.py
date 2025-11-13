from sqlmodel import Session, select
from app.models.group import Group
from fastapi import HTTPException

def create_group(group: Group, session: Session):
    session.add(group)
    session.commit()
    session.refresh(group)
    return group

def get_groups(session: Session):
    groups = session.exec(select(Group)).all()
    if not groups:
        raise HTTPException(status_code=404, detail="Группы не найдены")
    return groups

def update_group(id: int, group: Group, session: Session):
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

def delete_group(id: int, session: Session):
    db_group = session.get(Group, id)
    if not db_group:
        raise HTTPException(status_code=404, detail="Группа не найдена")
    session.delete(db_group)
    session.commit()
    return {"message": "Группа удалена"}
