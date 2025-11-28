from sqlmodel import SQLModel, create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import async_sessionmaker  # ← важно!
from dotenv import load_dotenv
import os


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not set")

# Асинхронный движок
engine = create_async_engine(DATABASE_URL, echo=True)

# Асинхронная фабрика сессий
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)

async def init_db(drop_all: bool = False):
    """Создание таблиц в базе данных"""
    # Импортируем все модели, чтобы SQLModel знал о них
    from app.models.specialty import Specialty
    from app.models.group import Group
    from app.models.discipline import Discipline
    from app.models.teacher import Teacher
    from app.models.workload import Workload
    from app.models.curriculum import Curriculum
    from app.models.lesson_type import LessonType
    from app.models.user import Users
    
    async with engine.begin() as conn:
        if drop_all:
            await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)

async def close_db():
    """Закрытие соединения с базой данных"""
    await engine.dispose()
