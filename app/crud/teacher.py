from sqlmodel import Session, select
from app.models import Teacher
from app.schemas.schemas import TeacherCreate, TeacherUpdate

def get_teacher(session: Session, teacher_id: int):
    return session.get(Teacher, teacher_id)

def get_teachers(session: Session, skip: int = 0, limit: int = 100):
    return session.exec(select(Teacher).offset(skip).limit(limit)).all()

def create_teacher(session: Session, teacher: TeacherCreate):
    db_teacher = Teacher.from_orm(teacher)
    session.add(db_teacher)
    session.commit()
    session.refresh(db_teacher)
    return db_teacher

def update_teacher(session: Session, teacher_id: int, teacher: TeacherUpdate):
    db_teacher = session.get(Teacher, teacher_id)
    if db_teacher:
        teacher_data = teacher.dict(exclude_unset=True)
        for key, value in teacher_data.items():
            setattr(db_teacher, key, value)
        session.add(db_teacher)
        session.commit()
        session.refresh(db_teacher)
    return db_teacher

def delete_teacher(session: Session, teacher_id: int):
    db_teacher = session.get(Teacher, teacher_id)
    if db_teacher:
        session.delete(db_teacher)
        session.commit()
    return db_teacher