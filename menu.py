import os
import sys
import subprocess
import config


def main_menu():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n" + "=" * 40)
        print("        ГЛАВНОЕ МЕНЮ")
        print("=" * 40)
        print("1. Сортировать")
        print("2. Настройки")
        print("3. Управление пресетами (по расширениям)")
        print("4. Управление ключевыми словами (по названию)")
        print("5. Об программе")
        print("6. Выход")
        print("=" * 40)

        choice = input("Выберите пункт меню (1-6): ")

        if choice == '1':
            show_sort_menu()
        elif choice == '2':
            os.system('cls' if os.name == 'nt' else 'clear')
            show_settings()
        elif choice == '3':
            os.system('cls' if os.name == 'nt' else 'clear')
            manage_presets()
        elif choice == '4':
            os.system('cls' if os.name == 'nt' else 'clear')
            manage_keywords()
        elif choice == '5':
            os.system('cls' if os.name == 'nt' else 'clear')
            show_about()
        elif choice == '6':
            print("\nДо свидания!")
            sys.exit()
        else:
            print("\nНеверный выбор. Пожалуйста, выберите 1-6.")
            input("Нажмите Enter для продолжения...")


def show_sort_menu():
    """Меню выбора режима сортировки"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n" + "=" * 40)
    print("        ВЫБОР РЕЖИМА СОРТИРОВКИ")
    print("=" * 40)
    print("1. Только по расширениям файлов")
    print("2. Только по ключевым словам в названии")
    print("3. Комбинированная (сначала ключевые слова, затем расширения)")
    print("4. Вернуться в главное меню")
    print("=" * 40)

    choice = input("Выберите режим (1-4): ")

    current_path = config.load_path_from_config()

    if not current_path:
        print("\nОшибка: Путь для сортировки не настроен!")
        print("Пожалуйста, сначала настройте путь в разделе 'Настройки'")
        input("\nНажмите Enter для возврата в меню...")
        return

    if not os.path.exists(current_path):
        print(f"\nОшибка: Папка '{current_path}' не существует!")
        print("Пожалуйста, проверьте путь в настройках")
        input("\nНажмите Enter для возврата в меню...")
        return

    mode = "both"
    if choice == '1':
        mode = "ext"
        mode_name = "только по расширениям"
    elif choice == '2':
        mode = "kw"
        mode_name = "только по ключевым словам"
    elif choice == '3':
        mode = "both"
        mode_name = "комбинированная"
    elif choice == '4':
        return
    else:
        print("\nНеверный выбор!")
        input("Нажмите Enter для продолжения...")
        return

    print(f"\nЗапуск сортировки в режиме: {mode_name}")

    try:
        subprocess.run([sys.executable, "main.py", current_path, mode], check=True)
    except subprocess.CalledProcessError:
        print("Ошибка при запуске сортировки")
    except FileNotFoundError:
        print("Файл main.py не найден")
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")
    input("\nНажмите Enter для возврата в меню...")


def show_settings():
    print("\n=== НАСТРОЙКИ ===")

    try:
        current_path = config.load_path_from_config()
        print(f"Текущая папка для сортировки: {current_path if current_path else 'Не указана'}")
        new_path = input("Введите новый путь для сортировки (или нажмите Enter, чтобы оставить текущий): ").strip()

        if new_path:
            if os.path.exists(new_path):
                if config.save_path_to_config(new_path):
                    print(f"Путь успешно изменен на: {new_path}")
                else:
                    print("Не удалось сохранить путь")
            else:
                print(f"Ошибка: Папка '{new_path}' не существует!")
        elif not current_path:
            print("Ошибка: Необходимо указать путь для сортировки!")

    except Exception as e:
        print(f"Произошла ошибка при изменении настроек: {e}")

    input("\nНажмите Enter для возврата в меню...")


def manage_presets():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n" + "=" * 40)
        print("     УПРАВЛЕНИЕ ПРЕСЕТАМИ (по расширениям)")
        print("=" * 40)

        # Показываем текущие пресеты
        presets = config.load_presets()
        print("\nТекущие правила сортировки по расширениям:")
        print("-" * 40)
        for folder, extensions in presets.items():
            if extensions:
                print(f"{folder}: {', '.join(extensions)}")
            else:
                print(f"{folder}: (все остальные файлы)")
        print("-" * 40)

        print("\nДоступные действия:")
        print("1. Добавить новый пресет")
        print("2. Редактировать пресет")
        print("3. Удалить пресет")
        print("4. Просмотреть файл пресетов")
        print("5. Сбросить к стандартным настройкам")
        print("6. Вернуться в главное меню")
        print("=" * 40)

        choice = input("Выберите действие (1-6): ")

        if choice == '1':
            add_new_preset()
        elif choice == '2':
            edit_preset()
        elif choice == '3':
            delete_preset()
        elif choice == '4':
            view_presets_file()
        elif choice == '5':
            reset_presets()
        elif choice == '6':
            break
        else:
            print("\nНеверный выбор!")
            input("Нажмите Enter для продолжения...")


def manage_keywords():
    """Управление ключевыми словами для сортировки по названию"""
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n" + "=" * 40)
        print("     УПРАВЛЕНИЕ КЛЮЧЕВЫМИ СЛОВАМИ (по названию)")
        print("=" * 40)

        # Показываем текущие ключевые слова
        keywords = config.load_keywords()
        print("\nТекущие правила сортировки по ключевым словам:")
        print("-" * 40)
        if keywords:
            for folder, words in keywords.items():
                print(f"{folder}: {', '.join(words)}")
        else:
            print("Нет настроенных ключевых слов")
        print("-" * 40)

        print("\nДоступные действия:")
        print("1. Добавить правило (папка + ключевые слова)")
        print("2. Редактировать правило")
        print("3. Удалить правило")
        print("4. Просмотреть файл ключевых слов")
        print("5. Очистить все правила")
        print("6. Вернуться в главное меню")
        print("=" * 40)

        choice = input("Выберите действие (1-6): ")

        if choice == '1':
            add_keyword_rule()
        elif choice == '2':
            edit_keyword_rule()
        elif choice == '3':
            delete_keyword_rule()
        elif choice == '4':
            view_keywords_file()
        elif choice == '5':
            clear_all_keywords()
        elif choice == '6':
            break
        else:
            print("\nНеверный выбор!")
            input("Нажмите Enter для продолжения...")


def add_keyword_rule():
    print("\n=== ДОБАВЛЕНИЕ ПРАВИЛА ПО КЛЮЧЕВЫМ СЛОВАМ ===\n")

    folder_name = input("Введите название папки для сортировки: ").strip()
    if not folder_name:
        print("Название папки не может быть пустым!")
        input("Нажмите Enter для продолжения...")
        return

    print("Введите ключевые слова через запятую (например: отчет, документ, важное):")
    keywords_input = input("Ключевые слова: ").strip()
    keywords_list = [kw.strip().lower() for kw in keywords_input.split(',') if kw.strip()]

    if not keywords_list:
        print("Необходимо указать хотя бы одно ключевое слово!")
        input("Нажмите Enter для продолжения...")
        return

    if config.add_keyword(folder_name, keywords_list):
        print(f"\nПравило для папки '{folder_name}' успешно добавлено!")
        print(f"Файлы с ключевыми словами {', '.join(keywords_list)} будут помещаться в папку '{folder_name}'")
    else:
        print("Ошибка при добавлении правила!")

    input("\nНажмите Enter для продолжения...")


def edit_keyword_rule():
    print("\n=== РЕДАКТИРОВАНИЕ ПРАВИЛА ПО КЛЮЧЕВЫМ СЛОВАМ ===\n")

    keywords = config.load_keywords()
    if not keywords:
        print("Нет настроенных правил для редактирования!")
        input("Нажмите Enter для продолжения...")
        return

    folder_list = list(keywords.keys())

    print("Доступные правила для редактирования:")
    for i, folder in enumerate(folder_list, 1):
        print(f"{i}. {folder} - {', '.join(keywords[folder])}")

    try:
        choice = int(input("\nВыберите номер правила для редактирования: "))
        if 1 <= choice <= len(folder_list):
            folder_name = folder_list[choice - 1]
            current_keywords = keywords[folder_name]
            print(f"\nТекущие ключевые слова для '{folder_name}': {', '.join(current_keywords)}")

            print("\nВведите новые ключевые слова через запятую (или нажмите Enter, чтобы оставить текущие):")
            keywords_input = input("Ключевые слова: ").strip()

            if keywords_input:
                new_keywords = [kw.strip().lower() for kw in keywords_input.split(',') if kw.strip()]
                if new_keywords:
                    if config.update_keywords(folder_name, new_keywords):
                        print(f"\nПравило для '{folder_name}' успешно обновлено!")
                        print(f"Новые ключевые слова: {', '.join(new_keywords)}")
                    else:
                        print("Ошибка при обновлении правила!")
                else:
                    print("Не указаны ключевые слова для обновления!")
            else:
                print("Изменения не сохранены!")
        else:
            print("Неверный номер!")
    except ValueError:
        print("Пожалуйста, введите корректный номер!")

    input("\nНажмите Enter для продолжения...")


def delete_keyword_rule():
    print("\n=== УДАЛЕНИЕ ПРАВИЛА ПО КЛЮЧЕВЫМ СЛОВАМ ===\n")

    keywords = config.load_keywords()
    if not keywords:
        print("Нет настроенных правил для удаления!")
        input("Нажмите Enter для продолжения...")
        return

    folder_list = list(keywords.keys())

    print("Доступные правила для удаления:")
    for i, folder in enumerate(folder_list, 1):
        print(f"{i}. {folder} - {', '.join(keywords[folder])}")

    try:
        choice = int(input("\nВыберите номер правила для удаления: "))
        if 1 <= choice <= len(folder_list):
            folder_name = folder_list[choice - 1]
            confirm = input(
                f"Вы уверены, что хотите удалить правило для папки '{folder_name}'? (да/нет): ").strip().lower()
            if confirm in ['да', 'yes', 'y', 'д']:
                if config.remove_keyword_rule(folder_name):
                    print(f"\nПравило для '{folder_name}' успешно удалено!")
                else:
                    print("Ошибка при удалении правила!")
            else:
                print("Удаление отменено!")
        else:
            print("Неверный номер!")
    except ValueError:
        print("Пожалуйста, введите корректный номер!")

    input("\nНажмите Enter для продолжения...")


def view_keywords_file():
    """Просмотр содержимого файла ключевых слов"""
    print("\n=== СОДЕРЖИМОЕ ФАЙЛА КЛЮЧЕВЫХ СЛОВ ===\n")
    content = config.view_keywords_file()
    print(content)
    print("\nФормат файла: Имя_папки=слово1,слово2,слово3")
    print("Файлы, содержащие любое из этих слов в названии, будут перемещены в указанную папку")
    input("\nНажмите Enter для продолжения...")


def clear_all_keywords():
    """Очистка всех правил по ключевым словам"""
    print("\n=== ОЧИСТКА ВСЕХ ПРАВИЛ ===\n")
    confirm = input("Вы уверены, что хотите удалить ВСЕ правила по ключевым словам? (да/нет): ").strip().lower()

    if confirm in ['да', 'yes', 'y', 'д']:
        if config.save_keywords({}):
            print("\nВсе правила успешно удалены!")
        else:
            print("Ошибка при удалении правил!")
    else:
        print("Очистка отменена!")

    input("\nНажмите Enter для продолжения...")


def add_new_preset():
    print("\n=== ДОБАВЛЕНИЕ НОВОГО ПРЕСЕТА ===\n")

    folder_name = input("Введите название папки для сортировки: ").strip()
    if not folder_name:
        print("Название папки не может быть пустым!")
        input("Нажмите Enter для продолжения...")
        return

    if folder_name in ["Images", "Documents", "Archives", "Other"]:
        print(f"Папка '{folder_name}' уже существует! Используйте редактирование для изменения.")
        input("Нажмите Enter для продолжения...")
        return

    print("Введите расширения файлов через запятую (например: mp3, mp4, avi):")
    extensions_input = input("Расширения: ").strip()
    extensions = [ext.strip().lower() for ext in extensions_input.split(',') if ext.strip()]

    if not extensions:
        print("Необходимо указать хотя бы одно расширение!")
        input("Нажмите Enter для продолжения...")
        return

    if config.add_preset(folder_name, extensions):
        print(f"\nПресет '{folder_name}' успешно добавлен!")
        print(f"Файлы с расширениями {', '.join(extensions)} будут помещаться в папку '{folder_name}'")
    else:
        print("Ошибка при добавлении пресета!")

    input("\nНажмите Enter для продолжения...")


def edit_preset():
    print("\n=== РЕДАКТИРОВАНИЕ ПРЕСЕТА ===\n")

    presets = config.load_presets()
    preset_list = list(presets.keys())

    print("Доступные пресеты для редактирования:")
    for i, preset in enumerate(preset_list, 1):
        if preset != "Other":
            print(f"{i}. {preset}")

    if len(preset_list) <= 1:
        print("Нет доступных пресетов для редактирования!")
        input("Нажмите Enter для продолжения...")
        return

    try:
        choice = int(input("\nВыберите номер пресета для редактирования: "))
        if 1 <= choice <= len(preset_list):
            folder_name = preset_list[choice - 1]
            if folder_name == "Other":
                print("Пресет 'Other' нельзя редактировать!")
                input("Нажмите Enter для продолжения...")
                return

            current_extensions = presets[folder_name]
            print(f"\nТекущие расширения для '{folder_name}': {', '.join(current_extensions)}")

            print("\nВведите новые расширения через запятую (или нажмите Enter, чтобы оставить текущие):")
            extensions_input = input("Расширения: ").strip()

            if extensions_input:
                new_extensions = [ext.strip().lower() for ext in extensions_input.split(',') if ext.strip()]
                if new_extensions:
                    if config.update_preset(folder_name, new_extensions):
                        print(f"\nПресет '{folder_name}' успешно обновлен!")
                        print(f"Новые расширения: {', '.join(new_extensions)}")
                    else:
                        print("Ошибка при обновлении пресета!")
                else:
                    print("Не указаны расширения для обновления!")
            else:
                print("Изменения не сохранены!")
        else:
            print("Неверный номер!")
    except ValueError:
        print("Пожалуйста, введите корректный номер!")

    input("\nНажмите Enter для продолжения...")


def delete_preset():
    print("\n=== УДАЛЕНИЕ ПРЕСЕТА ===\n")

    presets = config.load_presets()
    preset_list = [p for p in presets.keys() if p != "Other"]

    if not preset_list:
        print("Нет доступных пресетов для удаления!")
        input("Нажмите Enter для продолжения...")
        return

    print("Доступные пресеты для удаления:")
    for i, preset in enumerate(preset_list, 1):
        print(f"{i}. {preset}")

    try:
        choice = int(input("\nВыберите номер пресета для удаления: "))
        if 1 <= choice <= len(preset_list):
            folder_name = preset_list[choice - 1]
            confirm = input(f"Вы уверены, что хотите удалить пресет '{folder_name}'? (да/нет): ").strip().lower()
            if confirm in ['да', 'yes', 'y', 'д']:
                if config.remove_preset(folder_name):
                    print(f"\nПресет '{folder_name}' успешно удален!")
                else:
                    print("Ошибка при удалении пресета!")
            else:
                print("Удаление отменено!")
        else:
            print("Неверный номер!")
    except ValueError:
        print("Пожалуйста, введите корректный номер!")

    input("\nНажмите Enter для продолжения...")


def view_presets_file():
    print("\n=== СОДЕРЖИМОЕ ФАЙЛА ПРЕСЕТОВ ===\n")
    content = config.view_presets_file()
    print(content)
    print("\nФормат файла: Имя_папки=расширение1,расширение2,расширение3")
    input("\nНажмите Enter для продолжения...")


def reset_presets():
    print("\n=== СБРОС НАСТРОЕК ===\n")
    confirm = input("Вы уверены, что хотите сбросить все пресеты к стандартным? (да/нет): ").strip().lower()

    if confirm in ['да', 'yes', 'y', 'д']:
        default_presets = {
            "Images": ["jpg", "jpeg", "png", "gif", "bmp"],
            "Documents": ["pdf", "docx", "doc", "txt", "xlsx"],
            "Archives": ["zip", "rar", "7z"],
            "Other": []
        }
        if config.save_presets(default_presets):
            print("\nНастройки успешно сброшены до стандартных!")
        else:
            print("Ошибка при сбросе настроек!")
    else:
        print("Сброс отменен!")

    input("\nНажмите Enter для продолжения...")


def show_about():
    try:
        print("\n=== О ПРОГРАММЕ ===")
        print("Программа для автоматической сортировки файлов")
        print("Версия: 3.0")
        print("Автор: Ярослав Бекренёв")
        print("Назначение: сортировка файлов по категориям")
        print("\nДва способа сортировки:")
        print("1. ПО РАСШИРЕНИЯМ - файлы сортируются по типу (jpg, pdf, zip и т.д.)")
        print("2. ПО КЛЮЧЕВЫМ СЛОВАМ - файлы сортируются по наличию слов в названии")
        print("\nКак это работает:")
        print("1. Настройте путь для сортировки в разделе 'Настройки'")
        print("2. Настройте пресеты (правила сортировки) в соответствующих разделах")
        print("3. Выберите режим сортировки в главном меню")
        print("4. Файлы будут отсортированы по папкам")
        print("\nОсобенности:")
        print("- Можно использовать оба способа сортировки вместе")
        print("- При комбинированной сортировке сначала применяются ключевые слова")
        print("- Автоматическое разрешение конфликтов имен файлов")
        print("- Сохранение настроек между сеансами")
        print("- Пресеты хранятся в файлах presets.txt и keywords.txt")
    except Exception as e:
        print(f"Ошибка при отображении информации: {e}")
    input("\nНажмите Enter для возврата в меню...")


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем")
        sys.exit()
    except Exception as e:
        print(f"\nКритическая ошибка: {e}")
        input("Нажмите Enter для выхода...")
        sys.exit()
