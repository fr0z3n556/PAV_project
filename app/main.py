from controllers.teacher_controller import add_teacher, get_all_teachers, get_teacher_by_id
from controllers.teacher_auth_controller import register_teacher, authenticate_teacher, get_teacher_credentials
from views.teachers_view import show_teachers, input_teacher_data, input_teacher_id, show_operation_result
from views.teacher_auth_view import input_login_data, input_registration_data, show_auth_result, show_teacher_info
from bd.database import conn, cursor
import sys

def init_database():
    """Инициализация базы данных и создание таблицы для учетных данных, если её нет"""
    try:
        # Проверяем, существует ли таблица teacher_credentials
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'teacher_credentials'
            )
        """)
        table_exists = cursor.fetchone()[0]
        
        if not table_exists:
            # Создаем таблицу, если её нет
            cursor.execute("""
                CREATE TABLE teacher_credentials (
                    teacher_id INTEGER PRIMARY KEY REFERENCES teachers(teacher_id),
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            print("Таблица teacher_credentials создана успешно!")
        
        return True
    except Exception as e:
        print(f"Ошибка инициализации базы данных: {e}")
        return False

def auth_menu():
    """
    Меню аутентификации
    :return: teacher_id аутентифицированного пользователя или None
    """
    while True:
        print("\n=== Система аутентификации ===")
        print("1. Вход")
        print("2. Регистрация")
        print("3. Выход из программы")
        
        choice = input("Выберите действие: ").strip()
        
        if choice == "1":
            # Аутентификация
            username, password = input_login_data()
            teacher_id = authenticate_teacher(username, password)
            if teacher_id:
                show_auth_result(True)
                credentials = get_teacher_credentials(teacher_id)
                if credentials:
                    show_teacher_info(teacher_id, credentials[0])
                return teacher_id
            else:
                show_auth_result(False)
                
        elif choice == "2":
            # Регистрация
            teacher_id, username, password = input_registration_data()
            
            # Проверяем, существует ли преподаватель с таким ID
            teacher = get_teacher_by_id(int(teacher_id))
            if not teacher:
                print("Преподаватель с таким ID не существует!")
                continue
                
            success = register_teacher(int(teacher_id), username, password)
            show_auth_result(success, False)
            
        elif choice == "3":
            print("Выход из программы...")
            sys.exit(0)
            
        else:
            print("Неверный выбор, попробуйте снова")

def main_menu(teacher_id):
    """
    Основное меню системы после аутентификации
    :param teacher_id: ID аутентифицированного преподавателя
    """
    while True:
        print("\n=== Система управления преподавателями ===")
        print(f"Вы вошли как преподаватель ID: {teacher_id}")
        print("1. Добавить преподавателя")
        print("2. Показать всех преподавателей")
        print("3. Найти преподавателя по ID")
        print("4. Выйти из системы")
        
        choice = input("Ваш выбор: ").strip()
        
        if choice == "1":
            # Добавление преподавателя
            name, photo_path = input_teacher_data()
            success = add_teacher(name, photo_path)
            show_operation_result(success, "добавления преподавателя")
            
        elif choice == "2":
            # Показать всех преподавателей
            teachers = get_all_teachers()
            show_teachers(teachers)
            
        elif choice == "3":
            # Поиск преподавателя по ID
            teacher_id_search = input_teacher_id()
            teacher = get_teacher_by_id(teacher_id_search)
            if teacher:
                print(f"\nНайден преподаватель:")
                print(f"ID: {teacher[0]}, Имя: {teacher[1]}, Фото: {teacher[2] or 'нет'}")
            else:
                print(f"\nПреподаватель с ID {teacher_id_search} не найден")
                
        elif choice == "4":
            print("Выход из системы...")
            break
            
        else:
            print("Неверный выбор, попробуйте снова")

def main():
    """Основная функция программы"""
    print("=== Система управления преподавателями с аутентификацией ===")
    
    # Инициализация базы данных
    if not init_database():
        print("Не удалось инициализировать базу данных. Программа завершена.")
        return
    
    # Основной цикл программы
    while True:
        # Аутентификация
        teacher_id = auth_menu()
        
        if teacher_id:
            # Основное меню после успешной аутентификации
            main_menu(teacher_id)
        else:
            print("Аутентификация не удалась")

if __name__ == "__main__":
    main()