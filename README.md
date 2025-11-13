# Документация проекта

1. Создание и активация виртуального окружения

2. Создайте виртуальное окружение с помощью venv:

python -m venv venv


А затем активируйте его:

Для Windows (PowerShell):

.\venv\Scripts\Activate.ps1


Для Linux/Mac:

source venv/bin/activate

3. Установка зависимостей

Установите все зависимости проекта из файла requirements.txt:

pip install -r requirements.txt

4. Настройка переменных окружения

Создайте файл .env в корне проекта и добавьте настройки для базы данных и другие необходимые переменные. Пример содержимого файла:

DATABASE_URL=postgresql+psycopg2://postgres:password@localhost:5432/college
SECRET_KEY=your_secret_key

5. Запуск приложения

Запустите сервер FastAPI с помощью Uvicorn:

uvicorn app.main:app --reload


Теперь приложение доступно по адресу: http://127.0.0.1:8000

6. Тестирование приложения

Для запуска тестов используйте pytest:

pytest

7. API документация

Документация API доступна по адресу: http://127.0.0.1:8000/docs