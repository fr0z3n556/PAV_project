def input_login_data():
    """
    Ввод данных для входа
    :return: кортеж (username, password)
    """
    print("\n=== Аутентификация ===")
    username = input("Имя пользователя: ").strip()
    password = input("Пароль: ").strip()
    return username, password

def input_registration_data():
    """
    Ввод данных для регистрации
    :return: кортеж (teacher_id, username, password)
    """
    print("\n=== Регистрация преподавателя ===")
    teacher_id = input("ID преподавателя: ").strip()
    username = input("Имя пользователя: ").strip()
    password = input("Пароль: ").strip()
    return teacher_id, username, password

def show_auth_result(success, is_login=True):
    """
    Показать результат аутентификации/регистрации
    :param success: успех операции
    :param is_login: True для входа, False для регистрации
    """
    operation = "входа" if is_login else "регистрации"
    if success:
        print(f"{operation.capitalize()} прошло успешно!")
    else:
        print(f"Ошибка {operation}. Проверьте введенные данные.")

def show_teacher_info(teacher_id, username):
    """
    Показать информацию об учетной записи
    :param teacher_id: ID преподавателя
    :param username: имя пользователя
    """
    print(f"\nУчетная запись:")
    print(f"ID преподавателя: {teacher_id}")
    print(f"Имя пользователя: {username}")