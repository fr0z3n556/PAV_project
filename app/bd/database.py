import psycopg2
from psycopg2 import sql

def init_db():
    """
    Подключение к БД PostgreSQL
    :return: conn - подключение, cursor - курсор
    """
    try:
        conn = psycopg2.connect(
            database="project",
            user="postgres",
            password=" ",
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()
        # Проверяем подключение
        cursor.execute("SELECT 1")
        conn.commit()
        print("База данных инициализирована успешно!")
        return conn, cursor
    except psycopg2.Error as e:
        print(f"Ошибка инициализации базы данных: {e}")
        return None, None

# Создание подключения и курсора
conn, cursor = init_db()
if conn and cursor:
    print("Можно продолжать работу")
else:
    print("Не удалось подключиться к базе данных")