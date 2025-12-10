# Документация проекта

## 1. Откройте проект

## 2. Создайте виртуальное окружение с помощью venv:

python -m venv venv

venv\Scripts\activate

## 3. Установите все зависимости проекта из файла requirements.txt

pip install -r requirements.txt

pip install alembic

alembic init alembic

pip install email-validator

## 4. Настройка переменных окружения

Создайте файл `.env` со следующими переменными:

DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/db_name
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

## 5. Запуск приложения

Запустите сервер FastAPI с помощью Uvicorn:

uvicorn app.main:app --reload

Теперь приложение доступно по адресу: http://127.0.0.1:8000

## 6. Тестирование приложения

Для запуска тестов используйте pytest:

pytest

## 7. API документация

Документация API доступна по адресу: http://127.0.0.1:8000/docs
