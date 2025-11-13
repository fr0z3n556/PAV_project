from sqlmodel import create_engine, SQLModel
from dotenv import load_dotenv
import os

load_dotenv()  # Загружаем переменные из .env

DATABASE_URL = os.getenv("DATABASE_URL")
print(f"Попытка подключения к базе данных: {DATABASE_URL}")  # Добавлено сообщение на русском

engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    from app.models.specialty import Specialty
    from app.models.group import Group
    from app.models.discipline import Discipline
    from app.models.teacher import Teacher
    from app.models.workload import Workload
    print("Создание таблиц...")  # Сообщение на русском
    try:
        SQLModel.metadata.create_all(engine)
        print("Таблицы успешно созданы!")  # Сообщение на русском
    except Exception as e:
        print(f"Ошибка при создании таблиц: {e}")  # Ошибка на русском
