import os
from sqlmodel import create_engine, Session
from urllib.parse import quote_plus
from app.config import settings  # Импортируем настройки из config.py

# Экранируем специальные символы в пароле
escaped_password = quote_plus(settings.DB_PASSWORD)

# Формируем строку подключения к базе данных
DATABASE_URL = f"postgresql+psycopg2://{settings.DB_USER}:{escaped_password}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

# Создаем движок для работы с базой данных
engine = create_engine(DATABASE_URL, echo=False)

def get_session():
    """Создает и возвращает сессию для работы с базой данных"""
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    """Создает все таблицы в базе данных на основе моделей SQLModel"""
    from app.models import Teacher, TeacherCredentials, Discipline, Specialty, EducationForm, GroupType, Groups, TeacherWorkload
    from sqlmodel import SQLModel
    
    SQLModel.metadata.create_all(engine)