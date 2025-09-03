def show_teachers(teachers: list[tuple]):
    """
    Вывод списка преподавателей
    :param teachers: список кортежей с данными
    """
    print("\nСписок преподавателей:")
    print("-" * 50)
    for teacher in teachers:
        print(f"ID: {teacher[0]}, Имя: {teacher[1]}, Фото: {teacher[2] or 'нет'}")

def input_teacher_data() -> tuple:
    """
    Ввод данных преподавателя
    :return: (full_name, photo_path)
    """
    print("\nВведите данные преподавателя:")
    full_name = input("Полное имя: ").strip()
    photo_path = input("Путь к фото (опционально): ").strip()
    return (full_name, photo_path if photo_path else None)

def input_teacher_id() -> int:
    """
    Ввод ID преподавателя
    :return: числовой ID
    """
    try:
        return int(input("Введите ID преподавателя: ").strip())
    except ValueError:
        return 0

def show_operation_result(success: bool, operation: str):
    """
    Вывод результата операции
    :param success: статус операции
    :param operation: тип операции
    """
    status = "успешно выполнена" if success else "завершилась ошибкой"
    print(f"\nОперация {operation} {status}")