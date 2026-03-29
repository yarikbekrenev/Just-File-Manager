import os
import sys
import subprocess


def save_path_to_config(path):
    try:
        with open("config.txt", "w", encoding="utf-8") as f:
            f.write(path)
        return True
    except Exception as e:
        print(f"Не удалось сохранить конфигурацию: {e}")
        return False


def load_path_from_config():
    try:
        if os.path.exists("config.txt"):
            with open("config.txt", "r", encoding="utf-8") as f:
                return f.read().strip()
    except Exception as e:
        print(f"Не удалось загрузить конфигурацию: {e}")
    return ""


def main_menu():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n" + "=" * 40)
        print("        ГЛАВНОЕ МЕНЮ")
        print("=" * 40)
        print("1. Сортировать")
        print("2. Настройки")
        print("3. Об программе")
        print("4. Выход")
        print("=" * 40)

        choice = input("Выберите пункт меню (1-4): ")

        if choice == '1':
            os.system('cls' if os.name == 'nt' else 'clear')
            print("=== ЗАПУСК СОРТИРОВКИ ===\n")

            current_path = load_path_from_config()

            if not current_path:
                print("Ошибка: Путь для сортировки не настроен!")
                print("Пожалуйста, сначала настройте путь в разделе 'Настройки'")
                input("\nНажмите Enter для возврата в меню...")
                continue

            if not os.path.exists(current_path):
                print(f"Ошибка: Папка '{current_path}' не существует!")
                print("Пожалуйста, проверьте путь в настройках")
                input("\nНажмите Enter для возврата в меню...")
                continue

            try:
                subprocess.run(["python", "main.py", current_path], check=True)
            except subprocess.CalledProcessError:
                print("Ошибка при запуске сортировки")
            except FileNotFoundError:
                print("Файл main.py не найден")
            except Exception as e:
                print(f"Непредвиденная ошибка: {e}")
            input("\nНажмите Enter для возврата в меню...")

        elif choice == '2':
            os.system('cls' if os.name == 'nt' else 'clear')
            show_settings()
        elif choice == '3':
            os.system('cls' if os.name == 'nt' else 'clear')
            show_about()
        elif choice == '4':
            print("\nДо свидания!")
            sys.exit()
        else:
            print("\nНеверный выбор. Пожалуйста, выберите 1-4.")
            input("Нажмите Enter для продолжения...")


def show_settings():
    print("\n=== НАСТРОЙКИ ===")

    try:
        current_path = load_path_from_config()
        print(f"Текущая папка для сортировки: {current_path if current_path else 'Не указана'}")
        new_path = input("Введите новый путь для сортировки (или нажмите Enter, чтобы оставить текущий): ").strip()

        if new_path:
            if os.path.exists(new_path):
                if save_path_to_config(new_path):
                    print(f"Путь успешно изменен на: {new_path}")
                else:
                    print("Не удалось сохранить путь")
            else:
                print(f"Ошибка: Папка '{new_path}' не существует!")
        elif not current_path:
            print("Ошибка: Необходимо указать путь для сортировки!")

    except Exception as e:
        print(f"Произошла ошибка при изменении настроек: {e}")

    print("\nРасширения для Images: jpg, jpeg, png, gif, bmp")
    print("Расширения для Documents: pdf, docx, doc, txt, xlsx")
    print("Расширения для Archives: zip, rar, 7z")
    print("Остальные файлы попадают в папку Other")
    input("\nНажмите Enter для возврата в меню...")


def show_about():
    try:
        print("\n=== О ПРОГРАММЕ ===")
        print("Программа для автоматической сортировки файлов")
        print("Версия: 1.0")
        print("Автор: Ярослав Бекренёв")
        print("Назначение: сортировка файлов по категориям")
        print("\nКак это работает:")
        print("1. Настройте путь для сортировки в разделе 'Настройки'")
        print("2. Выберите 'Сортировать' для запуска")
        print("3. Файлы будут отсортированы по папкам в зависимости от расширения")
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