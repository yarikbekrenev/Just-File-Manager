import os

CONFIG_FILE = "config/config.txt"
PRESETS_FILE = "config/presets.txt"
KEYWORDS_FILE = "config/keywords.txt"


def save_path_to_config(path):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            f.write(path)
        return True
    except Exception as e:
        print(f"Не удалось сохранить конфигурацию: {e}")
        return False


def load_path_from_config():
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return f.read().strip()
    except Exception as e:
        print(f"Не удалось загрузить конфигурацию: {e}")
    return ""


def clear_config():
    try:
        if os.path.exists(CONFIG_FILE):
            os.remove(CONFIG_FILE)
        return True
    except Exception as e:
        print(f"Не удалось очистить конфигурацию: {e}")
        return False


def is_config_exists():
    try:
        if os.path.exists(CONFIG_FILE):
            path = load_path_from_config()
            return bool(path)
        return False
    except Exception:
        return False


# Функции для работы с пресетами (по расширениям)
def save_presets(presets):
    """Сохранение пресетов в TXT файл"""
    try:
        with open(PRESETS_FILE, "w", encoding="utf-8") as f:
            for folder_name, extensions in presets.items():
                if extensions:
                    extensions_str = ",".join(extensions)
                    f.write(f"{folder_name}={extensions_str}\n")
                else:
                    f.write(f"{folder_name}=\n")
        return True
    except Exception as e:
        print(f"Не удалось сохранить пресеты: {e}")
        return False


def load_presets():
    """Загрузка пресетов из TXT файла"""
    default_presets = {
        "Images": ["jpg", "jpeg", "png", "gif", "bmp"],
        "Documents": ["pdf", "docx", "doc", "txt", "xlsx"],
        "Archives": ["zip", "rar", "7z"],
        "Other": []
    }

    try:
        if os.path.exists(PRESETS_FILE):
            presets = {}
            with open(PRESETS_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        if "=" in line:
                            folder_name, extensions_str = line.split("=", 1)
                            if extensions_str:
                                extensions = [ext.strip().lower() for ext in extensions_str.split(",") if ext.strip()]
                            else:
                                extensions = []
                            presets[folder_name] = extensions

            # Проверяем, что все стандартные папки есть
            for key in default_presets:
                if key not in presets:
                    presets[key] = default_presets[key]

            return presets
    except Exception as e:
        print(f"Не удалось загрузить пресеты: {e}")
    return default_presets


def add_preset(folder_name, extensions):
    """Добавление нового пресета"""
    presets = load_presets()
    presets[folder_name] = [ext.strip().lower() for ext in extensions if ext.strip()]
    return save_presets(presets)


def remove_preset(folder_name):
    """Удаление пресета (кроме Other)"""
    if folder_name == "Other":
        return False

    presets = load_presets()
    if folder_name in presets:
        del presets[folder_name]
        return save_presets(presets)
    return False


def update_preset(folder_name, extensions):
    """Обновление существующего пресета"""
    presets = load_presets()
    if folder_name in presets:
        presets[folder_name] = [ext.strip().lower() for ext in extensions if ext.strip()]
        return save_presets(presets)
    return False


def view_presets_file():
    """Просмотр содержимого файла пресетов"""
    try:
        if os.path.exists(PRESETS_FILE):
            with open(PRESETS_FILE, "r", encoding="utf-8") as f:
                return f.read()
        else:
            return "Файл пресетов еще не создан"
    except Exception as e:
        return f"Ошибка при чтении файла: {e}"


# Функции для работы с ключевыми словами
def save_keywords(keywords):
    """Сохранение ключевых слов в TXT файл"""
    try:
        with open(KEYWORDS_FILE, "w", encoding="utf-8") as f:
            for folder_name, words in keywords.items():
                if words:
                    words_str = ",".join(words)
                    f.write(f"{folder_name}={words_str}\n")
                else:
                    f.write(f"{folder_name}=\n")
        return True
    except Exception as e:
        print(f"Не удалось сохранить ключевые слова: {e}")
        return False


def load_keywords():
    """Загрузка ключевых слов из TXT файла"""
    default_keywords = {}

    try:
        if os.path.exists(KEYWORDS_FILE):
            keywords = {}
            with open(KEYWORDS_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        if "=" in line:
                            folder_name, words_str = line.split("=", 1)
                            if words_str:
                                words = [word.strip().lower() for word in words_str.split(",") if word.strip()]
                            else:
                                words = []
                            keywords[folder_name] = words
            return keywords
    except Exception as e:
        print(f"Не удалось загрузить ключевые слова: {e}")
    return default_keywords


def add_keyword(folder_name, keywords_list):
    """Добавление нового правила по ключевым словам"""
    keywords = load_keywords()
    if folder_name in keywords:
        # Добавляем новые ключевые слова к существующим
        keywords[folder_name].extend([kw.strip().lower() for kw in keywords_list if kw.strip()])
        keywords[folder_name] = list(set(keywords[folder_name]))  # Удаляем дубликаты
    else:
        keywords[folder_name] = [kw.strip().lower() for kw in keywords_list if kw.strip()]
    return save_keywords(keywords)


def remove_keyword_rule(folder_name):
    """Удаление правила по ключевым словам"""
    keywords = load_keywords()
    if folder_name in keywords:
        del keywords[folder_name]
        return save_keywords(keywords)
    return False


def update_keywords(folder_name, keywords_list):
    """Обновление ключевых слов для папки"""
    keywords = load_keywords()
    keywords[folder_name] = [kw.strip().lower() for kw in keywords_list if kw.strip()]
    return save_keywords(keywords)


def view_keywords_file():
    """Просмотр содержимого файла ключевых слов"""
    try:
        if os.path.exists(KEYWORDS_FILE):
            with open(KEYWORDS_FILE, "r", encoding="utf-8") as f:
                return f.read()
        else:
            return "Файл ключевых слов еще не создан"
    except Exception as e:
        return f"Ошибка при чтении файла: {e}"