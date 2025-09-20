# Стандартные библиотеки Python
import logging
import os
import secrets
import time
from datetime import timedelta
from typing import Optional

# Сторонние библиотеки (FastAPI и связанные)
from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# Сторонние библиотеки (работа с базой данных)
from sqlmodel import Session, select

# Локальные импорты (модули вашего приложения)
from app.auth.auth import (authenticate_user, create_access_token,
                          get_password_hash, verify_password)
from app.config import settings
from app.db.database import create_db_and_tables, get_session
from app.models import Teacher, TeacherCredentials
from app.schemas.schemas import (TeacherCreate, TeacherCredentialsCreate,
                                TeacherRead, TeacherUpdate, Token)

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Импорты из текущего пакета
from app.db.database import get_session, create_db_and_tables
from app.models import Teacher, TeacherCredentials
from app.schemas.schemas import TeacherCreate, TeacherRead, TeacherUpdate, TeacherCredentialsCreate, Token
from app.auth.auth import authenticate_user, create_access_token, get_password_hash, verify_password
from app.config import settings

app = FastAPI(title="University Management System", version="1.0.0")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Корневая страница
@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <html>
        <head>
            <title>University Management System</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 40px;
                    line-height: 1.6;
                }
                .container {
                    max-width: 800px;
                    margin: 0 auto;
                }
                h1 {
                    color: #333;
                }
                .links {
                    margin-top: 20px;
                }
                .links a {
                    display: block;
                    margin: 10px 0;
                    color: #1a73e8;
                    text-decoration: none;
                }
                .links a:hover {
                    text-decoration: underline;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>University Management System</h1>
                <p>Добро пожаловать в систему управления ЕМК!</p>
                
                <div class="links">
                    <h2>Документация API:</h2>
                    <a href="/docs" target="_blank">Swagger UI Documentation</a>
                    <a href="/redoc" target="_blank">ReDoc Documentation</a>
                </div>
                
                <div class="links">
                    <h2>Доступные endpoint'ы:</h2>
                    <a href="/teachers/">GET /teachers/ - Список преподавателей</a>
                    <a href="/docs#/default/create_teacher_teachers__post">POST /teachers/ - Добавить преподавателя</a>
                    <a href="/docs#/default/create_credentials_teachers__teacher_id__credentials_post">POST /teachers/{id}/credentials - Создать учетные данные</a>
                    <a href="/docs#/default/login_for_access_token_token_post">POST /token - Аутентификация</a>
                </div>
            </div>
        </body>
    </html>
    """

@app.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"Request {request.method} {request.url} took: {process_time} seconds")
    return response

# Защищенные endpoint'ы требуют аутентификацию
@app.post("/teachers/", response_model=TeacherRead)
def create_teacher(teacher: TeacherCreate, session: Session = Depends(get_session), token: str = Depends(oauth2_scheme)):
    db_teacher = Teacher.from_orm(teacher)
    session.add(db_teacher)
    session.commit()
    session.refresh(db_teacher)
    return db_teacher

@app.get("/teachers/", response_model=list[TeacherRead])
def read_teachers(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    teachers = session.exec(select(Teacher).offset(skip).limit(limit)).all()
    return teachers

@app.put("/teachers/{teacher_id}", response_model=TeacherRead)
def update_teacher(teacher_id: int, teacher: TeacherUpdate, session: Session = Depends(get_session), token: str = Depends(oauth2_scheme)):
    db_teacher = session.get(Teacher, teacher_id)
    if db_teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    teacher_data = teacher.dict(exclude_unset=True)
    for key, value in teacher_data.items():
        setattr(db_teacher, key, value)
    
    session.add(db_teacher)
    session.commit()
    session.refresh(db_teacher)
    return db_teacher

@app.delete("/teachers/{teacher_id}")
def delete_teacher(teacher_id: int, session: Session = Depends(get_session), token: str = Depends(oauth2_scheme)):
    teacher = session.get(Teacher, teacher_id)
    if teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    session.delete(teacher)
    session.commit()
    return {"ok": True}

@app.exception_handler(Exception)
async def universal_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error", "detail": str(exc)},
    )

@app.post("/teachers/{teacher_id}/credentials")
def create_credentials(teacher_id: int, credentials: TeacherCredentialsCreate, session: Session = Depends(get_session), token: str = Depends(oauth2_scheme)):
    # Check if teacher exists
    teacher = session.get(Teacher, teacher_id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    # Check if credentials already exist
    existing_credentials = session.exec(select(TeacherCredentials).where(TeacherCredentials.teacher_id == teacher_id)).first()
    if existing_credentials:
        raise HTTPException(status_code=400, detail="Credentials already exist for this teacher")
    
    # Create credentials
    password_hash = get_password_hash(credentials.password)
    db_credentials = TeacherCredentials(
        teacher_id=teacher_id,
        username=credentials.username,
        password_hash=password_hash
    )
    session.add(db_credentials)
    session.commit()
    session.refresh(db_credentials)
    
    return {"message": "Credentials created successfully", "username": db_credentials.username}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)