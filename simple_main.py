import os
from sqlmodel import SQLModel, Field, create_engine, Session, select
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional

# Настройки базы данных
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", " ")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "project")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL, echo=True)

# Модели
class Teacher(SQLModel, table=True):
    __tablename__ = "teachers"
    
    teacher_id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str = Field(max_length=100)
    photo_path: Optional[str] = None

class TeacherCredentials(SQLModel, table=True):
    __tablename__ = "teacher_credentials"
    
    teacher_id: int = Field(foreign_key="teachers.teacher_id", primary_key=True)
    username: str = Field(max_length=50, unique=True)
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Функции для работы с паролями
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# Основная функция
def main():
    # Создаем таблицы
    SQLModel.metadata.create_all(engine)
    
    with Session(engine) as session:
        while True:
            print("\n=== Система управления преподавателями ===")
            print("1. Добавить преподавателя")
            print("2. Показать всех преподавателей")
            print("3. Зарегистрировать учетные данные")
            print("4. Выйти")
            
            choice = input("Выберите действие: ")
            
            if choice == "1":
                full_name = input("Полное имя: ")
                photo_path = input("Путь к фото (опционально): ") or None
                
                teacher = Teacher(full_name=full_name, photo_path=photo_path)
                session.add(teacher)
                session.commit()
                session.refresh(teacher)
                print(f"Преподаватель добавлен с ID: {teacher.teacher_id}")
                
            elif choice == "2":
                teachers = session.exec(select(Teacher)).all()
                for teacher in teachers:
                    print(f"ID: {teacher.teacher_id}, Имя: {teacher.full_name}")
                    
            elif choice == "3":
                teacher_id = int(input("ID преподавателя: "))
                username = input("Имя пользователя: ")
                password = input("Пароль: ")
                
                password_hash = get_password_hash(password)
                credentials = TeacherCredentials(
                    teacher_id=teacher_id,
                    username=username,
                    password_hash=password_hash
                )
                session.add(credentials)
                session.commit()
                print("Учетные данные созданы")
                
            elif choice == "4":
                print("Выход из программы")
                break
                
            else:
                print("Неверный выбор")

if __name__ == "__main__":
    main()