import psycopg2
from psycopg2 import sql
import hashlib
import secrets

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

def hash_password(password, salt=None):
    """
    Хеширование пароля с использованием salt
    :param password: пароль в чистом виде
    :param salt: соль (если нет, генерируется новая)
    :return: хеш пароля и соль
    """
    if salt is None:
        salt = secrets.token_hex(16)
    hashed_password = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    ).hex()
    return f"{salt}${hashed_password}"

def verify_password(stored_password, provided_password):
    """
    Проверка пароля
    :param stored_password: сохраненный хеш (соль$хеш)
    :param provided_password: предоставленный пароль
    :return: True если пароль верный, иначе False
    """
    salt, hashed = stored_password.split('$')
    new_hash = hash_password(provided_password, salt)
    return new_hash == stored_password

# Создание подключения и курсора
conn, cursor = init_db()
if conn and cursor:
    print("Можно продолжать работу")
else:
    print("Не удалось подключиться к базе данных")