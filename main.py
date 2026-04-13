import os
import shutil
import sys
import config

PATH_TO_SORT = ""


def sort_by_extension():
    print("\n--- Сортировка по расширениям ---")

    presets = config.load_presets()

    extension_to_folder = {}
    for folder, extensions in presets.items():
        for ext in extensions:
            if ext:
                extension_to_folder[ext] = folder

    all_items = os.listdir(PATH_TO_SORT)
    files_moved = 0
    errors = 0

    for item in all_items:
        item_full_path = os.path.join(PATH_TO_SORT, item)

        if os.path.isfile(item_full_path):
            try:
                if '.' in item:
                    extension = item.split('.')[-1].lower()
                else:
                    extension = ""

                target_folder = extension_to_folder.get(extension, "Other")

                target_folder_path = os.path.join(PATH_TO_SORT, target_folder)

                if not os.path.exists(target_folder_path):
                    os.makedirs(target_folder_path)
                    print(f"Создана папка: {target_folder}")

                target_file_path = os.path.join(target_folder_path, item)
                counter = 1
                while os.path.exists(target_file_path):
                    name, ext = os.path.splitext(item)
                    new_name = f"{name}_{counter}{ext}"
                    target_file_path = os.path.join(target_folder_path, new_name)
                    counter += 1

                shutil.move(item_full_path, target_file_path)
                files_moved += 1
                print(f"Файл '{item}' перемещен в папку '{target_folder}' (по расширению)")

            except Exception as e:
                errors += 1
                print(f"Не удалось обработать файл '{item}'. Ошибка: {e}")

    return files_moved, errors


def sort_by_keywords():
    """Сортировка по ключевым словам в названии файла"""
    print("\n--- Сортировка по ключевым словам ---")

    keywords = config.load_keywords()

    if not keywords:
        print("Нет настроенных ключевых слов для сортировки")
        return 0, 0

    all_items = os.listdir(PATH_TO_SORT)
    files_moved = 0
    errors = 0
    processed_files = set()

    for item in all_items:
        item_full_path = os.path.join(PATH_TO_SORT, item)

        if item in processed_files:
            continue

        if os.path.isfile(item_full_path):
            try:
                item_lower = item.lower()
                target_folder = None
                matched_keyword = None

                for folder, words in keywords.items():
                    for word in words:
                        if word.lower() in item_lower:
                            target_folder = folder
                            matched_keyword = word
                            break
                    if target_folder:
                        break

                if target_folder:
                    target_folder_path = os.path.join(PATH_TO_SORT, target_folder)

                    if not os.path.exists(target_folder_path):
                        os.makedirs(target_folder_path)
                        print(f"Создана папка: {target_folder}")

                    target_file_path = os.path.join(target_folder_path, item)
                    counter = 1
                    while os.path.exists(target_file_path):
                        name, ext = os.path.splitext(item)
                        new_name = f"{name}_{counter}{ext}"
                        target_file_path = os.path.join(target_folder_path, new_name)
                        counter += 1

                    shutil.move(item_full_path, target_file_path)
                    files_moved += 1
                    processed_files.add(item)
                    print(f"Файл '{item}' перемещен в папку '{target_folder}' (ключевое слово: '{matched_keyword}')")

            except Exception as e:
                errors += 1
                print(f"Не удалось обработать файл '{item}'. Ошибка: {e}")

    return files_moved, errors


def sort_files(sort_mode="both"):

    if not PATH_TO_SORT:
        print("Ошибка: Путь для сортировки не указан!")
        return

    if not os.path.exists(PATH_TO_SORT):
        print(f"Ошибка: Папка '{PATH_TO_SORT}' не существует!")
        return

    print(f"\nЗапуск сортировки в папке: {PATH_TO_SORT}")
    print(f"Режим сортировки: {sort_mode}")

    total_moved = 0
    total_errors = 0

    if sort_mode == "keywords":
        moved, errors = sort_by_keywords()
        total_moved += moved
        total_errors += errors

    elif sort_mode == "extension":
        moved, errors = sort_by_extension()
        total_moved += moved
        total_errors += errors

    elif sort_mode == "both":
        moved1, errors1 = sort_by_keywords()
        total_moved += moved1
        total_errors += errors1

        moved2, errors2 = sort_by_extension()
        total_moved += moved2
        total_errors += errors2

    print(f"\n{'=' * 40}")
    print(f"СОРТИРОВКА ЗАВЕРШЕНА!")
    print(f"Всего перемещено файлов: {total_moved}")
    if total_errors > 0:
        print(f"Ошибок при обработке: {total_errors}")
    print(f"{'=' * 40}")


if __name__ == "__main__":
    sort_mode = "both"

    if len(sys.argv) > 1:
        PATH_TO_SORT = sys.argv[1]
    else:
        PATH_TO_SORT = config.load_path_from_config()

    if len(sys.argv) > 2:
        mode_arg = sys.argv[2].lower()
        if mode_arg == "ext":
            sort_mode = "extension"
        elif mode_arg == "kw":
            sort_mode = "keywords"
        elif mode_arg == "both":
            sort_mode = "both"

    sort_files(sort_mode)
    input("\nНажмите Enter для выхода...")
