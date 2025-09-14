import os
from sqlmodel import create_engine, Session
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Экранируем специальные символы в пароле
escaped_password = quote_plus(DB_PASSWORD)

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{escaped_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=False)

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    from app.models.models import Teacher, TeacherCredentials
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)