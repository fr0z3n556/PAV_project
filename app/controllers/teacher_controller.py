from db.database import cursor, conn

def add_teacher(full_name: str, photo_path: str = None) -> bool:
    """
    Добавление преподавателя
    :param full_name: полное имя
    :param photo_path: путь к фото (опционально)
    :return: True при успешном добавлении
    """
    try:
        cursor.execute(
            "INSERT INTO teachers (full_name, photo_path) VALUES (%s, %s)",
            (full_name, photo_path)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Ошибка добавления: {e}")
        conn.rollback()
        return False

def get_teacher_by_id(teacher_id: int) -> tuple:
    """
    Поиск преподавателя по ID
    :return: кортеж с данными преподавателя
    """
    try:
        cursor.execute("SELECT * FROM teachers WHERE teacher_id = %s", (teacher_id,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Ошибка поиска: {e}")
        return None

def get_all_teachers() -> list[tuple]:
    """
    Получение всех преподавателей
    :return: список кортежей с данными
    """
    try:
        cursor.execute("SELECT * FROM teachers ORDER BY teacher_id")
        return cursor.fetchall()
    except Exception as e:
        print(f"Ошибка получения списка: {e}")
        return []