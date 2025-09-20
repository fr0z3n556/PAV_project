# Начало - создания приложение 01.09.2025 

## 01.09.2025 - Создал БД и связал таблицы

## 02.09.2025 - Подключил БД и таблицу "teacher" к Python - есть ошибка " Не удается разрешить импорт "psycopg2" из источника Pylance " 

P.s Исправлена 03.09.2025 , нужно сделать окружение , зайти через CMD в него и все загрузить " pip install psycopg "

## 03.09.2025 - Была добавлена функция хеширования пароля для таблицы "teacher" , для этого была созданна новая таблица "teacher_credentials" также исправленны ошибки по работе кода прошлые

## 14.09.2025 - Была добавлена библиотека ORM sqlmodel - Стало функционированное веб-приложение для преподователей ( Бубличная и Администратора ) Сейчас структур выглядит так на 14.09.2025 : 

<img width="257" height="912" alt="project" src="https://github.com/user-attachments/assets/08b78f37-4e8e-479b-a9aa-dd50cfa651f4" />

## 20.09.2025 - Реконструировать проект , изменил папку models на отдельные классы + добавил авто добавление ключа на 32 символа в .env Сейчас структур выглядит так на 20.09.2025 : 

<img width="419" height="849" alt="image" src="https://github.com/user-attachments/assets/23bc841b-a7ae-4985-9fdc-e2b1f13e5524" />

# ИНСТРУКЦИЯ
##  Как запустить :

### Скопировать проект с GitHub
git clone <ваш-репозиторий>
cd project

### Создать виртуальное окружение
python -m venv venv

### Создание ключа в .env
python -c "import secrets; print(secrets.token_hex(32))"

### Активировать виртуальное окружение
Для Windows:
venv\Scripts\activate
Для Linux/Mac:
source venv/bin/activate

### Установить зависимости
pip install -r requirements.txt

## Настроить .env

DB_USER=postgres
DB_PASSWORD=пароль_от_вашей_postgresql
DB_HOST=localhost
DB_PORT=5432
DB_NAME=project
SECRET_KEY=случайный_секретный_ключ_из_32_символов
ALGORITHM=HS256

## Запустить все :

### Вариант 1: Запуск веб-приложения
uvicorn app.main:app --reload

### Вариант 2: Запуск консольного приложения
python main.py

## Использование:

Веб-интерфейс : http://localhost:8000

Документация API : http://localhost:8000/docs

Альтернативная документация : http://localhost:8000/redoc
