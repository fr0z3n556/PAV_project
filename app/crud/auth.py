from sqlmodel import Session, select
from app.models import TeacherCredentials
from app.schemas.schemas import TeacherCredentialsCreate
from app.auth.auth import get_password_hash

def create_teacher_credentials(session: Session, credentials: TeacherCredentialsCreate, teacher_id: int):
    hashed_password = get_password_hash(credentials.password)
    db_credentials = TeacherCredentials(
        teacher_id=teacher_id,
        username=credentials.username,
        password_hash=hashed_password
    )
    session.add(db_credentials)
    session.commit()
    session.refresh(db_credentials)
    return db_credentials

def get_teacher_credentials(session: Session, teacher_id: int):
    return session.exec(select(TeacherCredentials).where(TeacherCredentials.teacher_id == teacher_id)).first()