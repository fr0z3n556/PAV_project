from bd.database import cursor, conn, hash_password, verify_password

def register_teacher(teacher_id, username, password):
    """
    Регистрация преподавателя в системе
    :param teacher_id: ID преподавателя
    :param username: имя пользователя
    :param password: пароль
    :return: True при успешной регистрации
    """
    try:
        # Проверяем, существует ли преподаватель
        cursor.execute("SELECT teacher_id FROM teachers WHERE teacher_id = %s", (teacher_id,))
        if not cursor.fetchone():
            return False
        
        # Хешируем пароль
        password_hash = hash_password(password)
        
        # Сохраняем учетные данные
        cursor.execute(
            "INSERT INTO teacher_credentials (teacher_id, username, password_hash) VALUES (%s, %s, %s)",
            (teacher_id, username, password_hash)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Ошибка регистрации: {e}")
        conn.rollback()
        return False

def authenticate_teacher(username, password):
    """
    Аутентификация преподавателя
    :param username: имя пользователя
    :param password: пароль
    :return: ID преподавателя при успешной аутентификации, иначе None
    """
    try:
        cursor.execute(
            "SELECT teacher_id, password_hash FROM teacher_credentials WHERE username = %s",
            (username,)
        )
        result = cursor.fetchone()
        
        if result and verify_password(result[1], password):
            return result[0]  # Возвращаем teacher_id
        return None
    except Exception as e:
        print(f"Ошибка аутентификации: {e}")
        return None

def get_teacher_credentials(teacher_id):
    """
    Получение учетных данных преподавателя
    :param teacher_id: ID преподавателя
    :return: учетные данные или None
    """
    try:
        cursor.execute(
            "SELECT username FROM teacher_credentials WHERE teacher_id = %s",
            (teacher_id,)
        )
        return cursor.fetchone()
    except Exception as e:
        print(f"Ошибка получения учетных данных: {e}")
        return None