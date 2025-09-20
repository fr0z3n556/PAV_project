import os
import sys
import requests
from pathlib import Path

# Добавляем папку app в путь Python
sys.path.append(str(Path(__file__).parent))

from app.db.database import get_session, create_db_and_tables
from app.models import Teacher, TeacherCredentials
from app.schemas.schemas import TeacherCreate, TeacherCredentialsCreate
from app.crud.teacher import create_teacher, get_teachers, get_teacher, update_teacher, delete_teacher
from app.crud.auth import create_teacher_credentials
from app.auth.auth import authenticate_user, get_password_hash

# Базовая URL для API
API_BASE_URL = "http://localhost:8000"

def get_auth_token(username, password):
    """Получение токена аутентификации"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/token",
            data={"username": username, "password": password},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        if response.status_code == 200:
            return response.json()["access_token"]
        else:
            print(f"Ошибка аутентификации: {response.status_code}")
            return None
    except Exception as e:
        print(f"Ошибка подключения к API: {e}")
        return None

def public_menu():
    """Меню для неавторизованных пользователей"""
    while True:
        print("\n=== Публичный доступ ===")
        print("1. Показать всех преподавателей")
        print("2. Найти преподавателя по ID")
        print("3. Войти в систему")
        print("4. Выйти")
        
        choice = input("Выберите действие: ")
        
        if choice == "1":
            # Получение списка преподавателей через API
            try:
                response = requests.get(f"{API_BASE_URL}/teachers/")
                if response.status_code == 200:
                    teachers = response.json()
                    for teacher in teachers:
                        print(f"ID: {teacher['teacher_id']}, Имя: {teacher['full_name']}, Фото: {teacher['photo_path']}")
                else:
                    print("Ошибка при получении данных")
            except Exception as e:
                print(f"Ошибка подключения: {e}")
                
        elif choice == "2":
            # Поиск преподавателя по ID
            try:
                teacher_id = int(input("ID преподавателя: "))
                response = requests.get(f"{API_BASE_URL}/teachers/{teacher_id}")
                if response.status_code == 200:
                    teacher = response.json()
                    print(f"ID: {teacher['teacher_id']}, Имя: {teacher['full_name']}, Фото: {teacher['photo_path']}")
                else:
                    print("Преподаватель не найден")
            except ValueError:
                print("Некорректный ID")
            except Exception as e:
                print(f"Ошибка подключения: {e}")
                
        elif choice == "3":
            # Аутентификация
            username = input("Имя пользователя: ")
            password = input("Пароль: ")
            
            token = get_auth_token(username, password)
            if token:
                print("Аутентификация успешна!")
                admin_menu(token)  # Переходим в меню администратора
            else:
                print("Ошибка аутентификации")
                
        elif choice == "4":
            print("Выход из программы")
            break
            
        else:
            print("Неверный выбор")

def admin_menu(token):
    """Меню для администраторов"""
    headers = {"Authorization": f"Bearer {token}"}
    
    while True:
        print("\n=== Панель администратора ===")
        print("1. Добавить преподавателя")
        print("2. Показать всех преподавателей")
        print("3. Найти преподавателя по ID")
        print("4. Обновить данные преподавателя")
        print("5. Удалить преподавателя")
        print("6. Зарегистрировать учетные данные преподавателя")
        print("7. Выйти из системы")
        
        choice = input("Выберите действие: ")
        
        if choice == "1":
            # Добавление преподавателя через API
            full_name = input("Полное имя: ")
            photo_path = input("Путь к фото (опционально): ") or None
            
            teacher_data = {"full_name": full_name, "photo_path": photo_path}
            try:
                response = requests.post(
                    f"{API_BASE_URL}/teachers/",
                    json=teacher_data,
                    headers=headers
                )
                if response.status_code == 200:
                    teacher = response.json()
                    print(f"Преподаватель добавлен с ID: {teacher['teacher_id']}")
                else:
                    print(f"Ошибка при добавлении: {response.status_code}")
            except Exception as e:
                print(f"Ошибка подключения: {e}")
                
        elif choice == "2":
            # Получение списка преподавателей через API
            try:
                response = requests.get(f"{API_BASE_URL}/teachers/", headers=headers)
                if response.status_code == 200:
                    teachers = response.json()
                    for teacher in teachers:
                        print(f"ID: {teacher['teacher_id']}, Имя: {teacher['full_name']}, Фото: {teacher['photo_path']}")
                else:
                    print(f"Ошибка при получении данных: {response.status_code}")
            except Exception as e:
                print(f"Ошибка подключения: {e}")
                
        elif choice == "3":
            # Поиск преподавателя по ID
            try:
                teacher_id = int(input("ID преподавателя: "))
                response = requests.get(f"{API_BASE_URL}/teachers/{teacher_id}", headers=headers)
                if response.status_code == 200:
                    teacher = response.json()
                    print(f"ID: {teacher['teacher_id']}, Имя: {teacher['full_name']}, Фото: {teacher['photo_path']}")
                else:
                    print("Преподаватель не найден")
            except ValueError:
                print("Некорректный ID")
            except Exception as e:
                print(f"Ошибка подключения: {e}")
                
        elif choice == "7":
            print("Выход из системы администратора")
            break
            
        else:
            print("Неверный выбор")

def main():
    # Создаем таблицы в базе данных
    create_db_and_tables()
    
    # Начинаем с публичного меню
    public_menu()

if __name__ == "__main__":
    main()