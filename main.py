import os
import shutil
import sys

PATH_TO_SORT = ""


def sort_files():
    if not PATH_TO_SORT:
        print("Ошибка: Путь для сортировки не указан!")
        return

    if not os.path.exists(PATH_TO_SORT):
        print(f"Ошибка: Папка '{PATH_TO_SORT}' не существует!")
        return

    all_items = os.listdir(PATH_TO_SORT)

    for item in all_items:
        item_full_path = os.path.join(PATH_TO_SORT, item)

        if os.path.isfile(item_full_path):
            try:
                extension = item.split('.')[-1].lower()

                target_folder = ''
                if extension in ['jpg', 'jpeg', 'png', 'gif', 'bmp']:
                    target_folder = 'Images'
                elif extension in ['pdf', 'docx', 'doc', 'txt', 'xlsx']:
                    target_folder = 'Documents'
                elif extension in ['zip', 'rar', '7z']:
                    target_folder = 'Archives'
                else:
                    target_folder = 'Other'

                target_folder_path = os.path.join(PATH_TO_SORT, target_folder)

                if not os.path.exists(target_folder_path):
                    os.makedirs(target_folder_path)
                    print(f"Создана папка: {target_folder}")

                shutil.move(item_full_path, target_folder_path)
                print(f"Файл '{item}' перемещен в папку '{target_folder}'")

            except Exception as e:
                print(f"Не удалось обработать файл '{item}'. Ошибка: {e}")

    print("\nСортировка завершена!")


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


if __name__ == "__main__":
    if len(sys.argv) > 1:
        PATH_TO_SORT = sys.argv[1]
    else:
        PATH_TO_SORT = load_path_from_config()

    sort_files()
    input("Нажмите Enter для выхода...")