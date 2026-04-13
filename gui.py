import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import sys
import shutil
import threading
import config


class FileSorterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Just File Manager")
        self.root.geometry("900x700")
        self.root.resizable(True, True)

        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass

        # Переменные для хранения состояния
        self.current_path = tk.StringVar()
        self.sort_mode = tk.StringVar(value="both")
        self.sort_in_progress = False

        # Загружаем сохраненный путь
        self.load_saved_path()

        # Создаем интерфейс
        self.create_widgets()

        # Обновляем статус
        self.update_status()

    def load_saved_path(self):
        """Загрузка сохраненного пути из конфига"""
        saved_path = config.load_path_from_config()
        if saved_path and os.path.exists(saved_path):
            self.current_path.set(saved_path)

    def create_widgets(self):
        """Создание всех виджетов интерфейса"""

        # Создаем вкладки
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=5, pady=5)

        # Вкладка сортировки
        self.sort_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.sort_tab, text="Сортировка")
        self.create_sort_tab()

        # Вкладка пресетов (по расширениям)
        self.presets_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.presets_tab, text="Пресеты (расширения)")
        self.create_presets_tab()

        # Вкладка ключевых слов
        self.keywords_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.keywords_tab, text="Ключевые слова")
        self.create_keywords_tab()

        # Вкладка информации
        self.info_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.info_tab, text="О программе")
        self.create_info_tab()

        # Статус бар
        self.status_bar = ttk.Label(self.root, text="Готов к работе", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def create_sort_tab(self):
        """Создание вкладки сортировки"""
        # Основной фрейм
        main_frame = ttk.Frame(self.sort_tab, padding="10")
        main_frame.pack(fill='both', expand=True)

        # Выбор папки
        path_frame = ttk.LabelFrame(main_frame, text="Выбор папки для сортировки", padding="10")
        path_frame.pack(fill='x', pady=(0, 10))

        ttk.Label(path_frame, text="Путь к папке:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        path_entry = ttk.Entry(path_frame, textvariable=self.current_path, width=60)
        path_entry.grid(row=0, column=1, sticky='ew', padx=(0, 5))

        ttk.Button(path_frame, text="Обзор...", command=self.browse_folder).grid(row=0, column=2)
        ttk.Button(path_frame, text="Сохранить путь", command=self.save_path).grid(row=0, column=3, padx=(5, 0))

        path_frame.columnconfigure(1, weight=1)

        # Режим сортировки
        mode_frame = ttk.LabelFrame(main_frame, text="Режим сортировки", padding="10")
        mode_frame.pack(fill='x', pady=(0, 10))

        ttk.Radiobutton(mode_frame, text="Только по расширениям", variable=self.sort_mode, value="ext").pack(
            anchor=tk.W)
        ttk.Radiobutton(mode_frame, text="Только по ключевым словам", variable=self.sort_mode, value="kw").pack(
            anchor=tk.W)
        ttk.Radiobutton(mode_frame, text="Комбинированная (сначала ключевые слова, затем расширения)",
                        variable=self.sort_mode, value="both").pack(anchor=tk.W)

        # Кнопка запуска сортировки
        self.sort_button = ttk.Button(main_frame, text="НАЧАТЬ СОРТИРОВКУ", command=self.start_sorting,
                                      style="Accent.TButton")
        self.sort_button.pack(pady=20)

        # Прогресс бар
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill='x', pady=(0, 10))

        # Лог сортировки
        log_frame = ttk.LabelFrame(main_frame, text="Лог сортировки", padding="10")
        log_frame.pack(fill='both', expand=True)

        self.log_text = tk.Text(log_frame, height=15, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)

        self.log_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Кнопки управления логом
        log_buttons_frame = ttk.Frame(log_frame)
        log_buttons_frame.pack(fill='x', pady=(5, 0))
        ttk.Button(log_buttons_frame, text="Очистить лог", command=self.clear_log).pack(side='right', padx=(5, 0))
        ttk.Button(log_buttons_frame, text="Сохранить лог", command=self.save_log).pack(side='right')

    def create_presets_tab(self):
        """Создание вкладки управления пресетами (по расширениям)"""
        # Основной фрейм
        main_frame = ttk.Frame(self.presets_tab, padding="10")
        main_frame.pack(fill='both', expand=True)

        # Список пресетов
        presets_frame = ttk.LabelFrame(main_frame, text="Пресеты (правила по расширениям)", padding="10")
        presets_frame.pack(fill='both', expand=True)

        # Создаем Treeview для отображения пресетов
        columns = ("Папка", "Расширения")
        self.presets_tree = ttk.Treeview(presets_frame, columns=columns, show="headings", height=10)
        self.presets_tree.heading("Папка", text="Папка назначения")
        self.presets_tree.heading("Расширения", text="Расширения файлов")
        self.presets_tree.column("Папка", width=150)
        self.presets_tree.column("Расширения", width=400)

        scrollbar = ttk.Scrollbar(presets_frame, orient="vertical", command=self.presets_tree.yview)
        self.presets_tree.configure(yscrollcommand=scrollbar.set)

        self.presets_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill='x', pady=(10, 0))

        ttk.Button(buttons_frame, text="Добавить", command=self.add_preset).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="Редактировать", command=self.edit_preset).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="Удалить", command=self.delete_preset).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="Обновить", command=self.refresh_presets).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="Сбросить к стандартным", command=self.reset_presets).pack(side='left', padx=5)

        self.refresh_presets()

    def create_keywords_tab(self):
        main_frame = ttk.Frame(self.keywords_tab, padding="10")
        main_frame.pack(fill='both', expand=True)

        keywords_frame = ttk.LabelFrame(main_frame, text="Ключевые слова (правила по названию)", padding="10")
        keywords_frame.pack(fill='both', expand=True)

        columns = ("Папка", "Ключевые слова")
        self.keywords_tree = ttk.Treeview(keywords_frame, columns=columns, show="headings", height=10)
        self.keywords_tree.heading("Папка", text="Папка назначения")
        self.keywords_tree.heading("Ключевые слова", text="Ключевые слова в названии")
        self.keywords_tree.column("Папка", width=150)
        self.keywords_tree.column("Ключевые слова", width=400)

        scrollbar = ttk.Scrollbar(keywords_frame, orient="vertical", command=self.keywords_tree.yview)
        self.keywords_tree.configure(yscrollcommand=scrollbar.set)

        self.keywords_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill='x', pady=(10, 0))

        ttk.Button(buttons_frame, text="Добавить", command=self.add_keyword_rule).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="Редактировать", command=self.edit_keyword_rule).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="Удалить", command=self.delete_keyword_rule).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="Обновить", command=self.refresh_keywords).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="Очистить все", command=self.clear_all_keywords).pack(side='left', padx=5)

        self.refresh_keywords()

    def create_info_tab(self):
        info_frame = ttk.Frame(self.info_tab, padding="20")
        info_frame.pack(fill='both', expand=True)

        title_label = ttk.Label(info_frame, text="Just File Manager",
                                font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 10))

        version_label = ttk.Label(info_frame, text="Версия 3.0", font=('Arial', 10))
        version_label.pack()

        author_label = ttk.Label(info_frame, text="Автор: Ярослав Бекренёв", font=('Arial', 10))
        author_label.pack(pady=(0, 20))

        # Описание
        desc_frame = ttk.LabelFrame(info_frame, text="О программе", padding="10")
        desc_frame.pack(fill='both', expand=True, pady=(0, 10))

        description = """
        Программа для автоматической сортировки файлов по двум типам правил:

        1. ПО РАСШИРЕНИЯМ:
           - Файлы сортируются по их расширению (.jpg, .pdf, .zip и т.д.)
           - Можно создавать свои правила для любых расширений

        2. ПО КЛЮЧЕВЫМ СЛОВАМ:
           - Файлы сортируются по наличию ключевых слов в названии
           - Не чувствительны к регистру

        3. КОМБИНИРОВАННЫЙ РЕЖИМ:
           - Сначала применяются правила по ключевым словам
           - Затем оставшиеся файлы сортируются по расширениям

        Особенности:
        • Автоматическое разрешение конфликтов имен
        • Сохранение всех настроек между сеансами
        • Удобный графический интерфейс
        • Подробный лог сортировки
        """

        desc_label = ttk.Label(desc_frame, text=description, justify=tk.LEFT)
        desc_label.pack(anchor=tk.W)

        # Файлы конфигурации
        config_frame = ttk.LabelFrame(info_frame, text="Файлы конфигурации", padding="10")
        config_frame.pack(fill='x')

        ttk.Label(config_frame, text="config.txt - путь для сортировки").pack(anchor=tk.W)
        ttk.Label(config_frame, text="presets.txt - правила по расширениям").pack(anchor=tk.W)
        ttk.Label(config_frame, text="keywords.txt - правила по ключевым словам").pack(anchor=tk.W)

    def browse_folder(self):
        folder = filedialog.askdirectory(title="Выберите папку для сортировки")
        if folder:
            self.current_path.set(folder)
            self.update_status()

    def save_path(self):
        path = self.current_path.get().strip()
        if path:
            if os.path.exists(path):
                if config.save_path_to_config(path):
                    self.add_to_log(f"Путь сохранен: {path}", "info")
                    self.update_status()
                else:
                    messagebox.showerror("Ошибка", "Не удалось сохранить путь!")
            else:
                messagebox.showerror("Ошибка", "Указанная папка не существует!")
        else:
            messagebox.showwarning("Предупреждение", "Путь не указан!")

    def update_status(self):
        path = self.current_path.get()
        if path and os.path.exists(path):
            self.status_bar.config(text=f"Текущая папка: {path}")
        elif path:
            self.status_bar.config(text=f"Ошибка: папка '{path}' не существует!")
        else:
            self.status_bar.config(text="Путь не указан. Выберите папку для сортировки.")

    def add_to_log(self, message, msg_type="info"):
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()

    def clear_log(self):
        self.log_text.delete(1.0, tk.END)

    def save_log(self):
        file_path = filedialog.asksaveasfilename(
            title="Сохранить лог",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.log_text.get(1.0, tk.END))
                messagebox.showinfo("Успех", "Лог успешно сохранен!")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить лог: {e}")

    def start_sorting(self):
        if self.sort_in_progress:
            messagebox.showwarning("Предупреждение", "Сортировка уже выполняется!")
            return

        path = self.current_path.get().strip()
        if not path:
            messagebox.showerror("Ошибка", "Пожалуйста, выберите папку для сортировки!")
            return

        if not os.path.exists(path):
            messagebox.showerror("Ошибка", f"Папка '{path}' не существует!")
            return

        self.clear_log()

        self.sort_in_progress = True
        self.sort_button.config(state='disabled', text="СОРТИРОВКА ВЫПОЛНЯЕТСЯ...")
        self.progress_var.set(0)

        thread = threading.Thread(target=self.run_sorting, args=(path,))
        thread.daemon = True
        thread.start()

    def run_sorting(self, path):
        try:
            mode = self.sort_mode.get()
            mode_names = {
                "ext": "только по расширениям",
                "kw": "только по ключевым словам",
                "both": "комбинированная"
            }

            self.add_to_log(f"{'=' * 60}", "info")
            self.add_to_log(f"ЗАПУСК СОРТИРОВКИ", "info")
            self.add_to_log(f"Папка: {path}", "info")
            self.add_to_log(f"Режим: {mode_names.get(mode, mode)}", "info")
            self.add_to_log(f"{'=' * 60}\n", "info")

            if mode == "ext":
                self.sort_by_extension(path)
            elif mode == "kw":
                self.sort_by_keywords(path)
            else:  # both
                self.sort_by_keywords(path)
                self.add_to_log("\n--- Переходим к сортировке по расширениям ---\n", "info")
                self.sort_by_extension(path)

            self.add_to_log(f"\n{'=' * 60}", "info")
            self.add_to_log("СОРТИРОВКА ЗАВЕРШЕНА!", "info")
            self.add_to_log(f"{'=' * 60}", "info")

            messagebox.showinfo("Завершено", "Сортировка успешно завершена!")

        except Exception as e:
            self.add_to_log(f"КРИТИЧЕСКАЯ ОШИБКА: {e}", "error")
            messagebox.showerror("Ошибка", f"Произошла ошибка при сортировке:\n{e}")
        finally:
            self.sort_in_progress = False
            self.sort_button.config(state='normal', text="НАЧАТЬ СОРТИРОВКУ")
            self.progress_var.set(100)

    def sort_by_extension(self, path):
        presets = config.load_presets()

        extension_to_folder = {}
        for folder, extensions in presets.items():
            for ext in extensions:
                if ext:
                    extension_to_folder[ext] = folder

        all_items = os.listdir(path)
        files = [item for item in all_items if os.path.isfile(os.path.join(path, item))]

        if not files:
            self.add_to_log("Нет файлов для сортировки по расширениям", "warning")
            return

        total = len(files)
        for i, item in enumerate(files):
            item_full_path = os.path.join(path, item)

            try:
                if '.' in item:
                    extension = item.split('.')[-1].lower()
                else:
                    extension = ""

                target_folder = extension_to_folder.get(extension, "Other")
                target_folder_path = os.path.join(path, target_folder)

                if not os.path.exists(target_folder_path):
                    os.makedirs(target_folder_path)

                target_file_path = os.path.join(target_folder_path, item)
                counter = 1
                while os.path.exists(target_file_path):
                    name, ext = os.path.splitext(item)
                    new_name = f"{name}_{counter}{ext}"
                    target_file_path = os.path.join(target_folder_path, new_name)
                    counter += 1

                shutil.move(item_full_path, target_file_path)
                self.add_to_log(f"✓ {item} -> {target_folder} (по расширению .{extension})", "success")

            except Exception as e:
                self.add_to_log(f"✗ Ошибка при обработке {item}: {e}", "error")

            progress = (i + 1) / total * 100
            self.progress_var.set(progress)
            self.root.update_idletasks()

    def sort_by_keywords(self, path):
        keywords = config.load_keywords()

        if not keywords:
            self.add_to_log("Нет настроенных ключевых слов для сортировки", "warning")
            return

        all_items = os.listdir(path)
        files = [item for item in all_items if os.path.isfile(os.path.join(path, item))]

        if not files:
            self.add_to_log("Нет файлов для сортировки по ключевым словам", "warning")
            return

        total = len(files)
        processed_files = set()

        for i, item in enumerate(files):
            if item in processed_files:
                continue

            item_full_path = os.path.join(path, item)

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
                    target_folder_path = os.path.join(path, target_folder)

                    if not os.path.exists(target_folder_path):
                        os.makedirs(target_folder_path)

                    target_file_path = os.path.join(target_folder_path, item)
                    counter = 1
                    while os.path.exists(target_file_path):
                        name, ext = os.path.splitext(item)
                        new_name = f"{name}_{counter}{ext}"
                        target_file_path = os.path.join(target_folder_path, new_name)
                        counter += 1

                    shutil.move(item_full_path, target_file_path)
                    self.add_to_log(f"✓ {item} -> {target_folder} (ключевое слово: '{matched_keyword}')", "success")
                    processed_files.add(item)

            except Exception as e:
                self.add_to_log(f"✗ Ошибка при обработке {item}: {e}", "error")

            progress = (i + 1) / total * 100
            self.progress_var.set(progress)
            self.root.update_idletasks()

    def refresh_presets(self):
        for item in self.presets_tree.get_children():
            self.presets_tree.delete(item)

        presets = config.load_presets()
        for folder, extensions in presets.items():
            if extensions:
                self.presets_tree.insert("", "end", values=(folder, ", ".join(extensions)))
            else:
                self.presets_tree.insert("", "end", values=(folder, "(все остальные файлы)"))

    def add_preset(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить пресет")
        dialog.geometry("400x250")
        dialog.resizable(False, False)

        ttk.Label(dialog, text="Название папки:").pack(pady=(10, 5))
        folder_entry = ttk.Entry(dialog, width=40)
        folder_entry.pack(pady=(0, 10))

        ttk.Label(dialog, text="Расширения (через запятую):").pack(pady=(0, 5))
        extensions_entry = ttk.Entry(dialog, width=40)
        extensions_entry.pack(pady=(0, 10))

        ttk.Label(dialog, text="Пример: jpg, png, pdf", foreground="gray").pack()

        def save():
            folder = folder_entry.get().strip()
            extensions_text = extensions_entry.get().strip()

            if not folder:
                messagebox.showwarning("Предупреждение", "Введите название папки!")
                return

            if not extensions_text:
                messagebox.showwarning("Предупреждение", "Введите хотя бы одно расширение!")
                return

            extensions = [ext.strip().lower() for ext in extensions_text.split(',') if ext.strip()]

            if config.add_preset(folder, extensions):
                messagebox.showinfo("Успех", f"Пресет '{folder}' добавлен!")
                self.refresh_presets()
                dialog.destroy()
            else:
                messagebox.showerror("Ошибка", "Не удалось добавить пресет!")

        ttk.Button(dialog, text="Сохранить", command=save).pack(pady=10)

    def edit_preset(self):
        selected = self.presets_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите пресет для редактирования!")
            return

        item = self.presets_tree.item(selected[0])
        folder_name = item['values'][0]

        if folder_name == "Other":
            messagebox.showwarning("Предупреждение", "Пресет 'Other' нельзя редактировать!")
            return

        presets = config.load_presets()
        current_extensions = presets.get(folder_name, [])

        dialog = tk.Toplevel(self.root)
        dialog.title(f"Редактировать пресет - {folder_name}")
        dialog.geometry("400x250")
        dialog.resizable(False, False)

        ttk.Label(dialog, text=f"Папка: {folder_name}").pack(pady=(10, 5))

        ttk.Label(dialog, text="Расширения (через запятую):").pack(pady=(0, 5))
        extensions_entry = ttk.Entry(dialog, width=40)
        extensions_entry.insert(0, ", ".join(current_extensions))
        extensions_entry.pack(pady=(0, 10))

        ttk.Label(dialog, text="Пример: jpg, png, pdf", foreground="gray").pack()

        def save():
            extensions_text = extensions_entry.get().strip()

            if not extensions_text:
                messagebox.showwarning("Предупреждение", "Введите хотя бы одно расширение!")
                return

            extensions = [ext.strip().lower() for ext in extensions_text.split(',') if ext.strip()]

            if config.update_preset(folder_name, extensions):
                messagebox.showinfo("Успех", f"Пресет '{folder_name}' обновлен!")
                self.refresh_presets()
                dialog.destroy()
            else:
                messagebox.showerror("Ошибка", "Не удалось обновить пресет!")

        ttk.Button(dialog, text="Сохранить", command=save).pack(pady=10)

    def delete_preset(self):
        selected = self.presets_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите пресет для удаления!")
            return

        item = self.presets_tree.item(selected[0])
        folder_name = item['values'][0]

        if folder_name == "Other":
            messagebox.showwarning("Предупреждение", "Пресет 'Other' нельзя удалить!")
            return

        if messagebox.askyesno("Подтверждение", f"Удалить пресет '{folder_name}'?"):
            if config.remove_preset(folder_name):
                messagebox.showinfo("Успех", f"Пресет '{folder_name}' удален!")
                self.refresh_presets()
            else:
                messagebox.showerror("Ошибка", "Не удалось удалить пресет!")

    def reset_presets(self):
        if messagebox.askyesno("Подтверждение", "Сбросить все пресеты к стандартным?"):
            default_presets = {
                "Images": ["jpg", "jpeg", "png", "gif", "bmp"],
                "Documents": ["pdf", "docx", "doc", "txt", "xlsx"],
                "Archives": ["zip", "rar", "7z"],
                "Other": []
            }
            if config.save_presets(default_presets):
                messagebox.showinfo("Успех", "Пресеты сброшены к стандартным!")
                self.refresh_presets()
            else:
                messagebox.showerror("Ошибка", "Не удалось сбросить пресеты!")

    def refresh_keywords(self):
        for item in self.keywords_tree.get_children():
            self.keywords_tree.delete(item)

        keywords = config.load_keywords()
        for folder, words in keywords.items():
            if words:
                self.keywords_tree.insert("", "end", values=(folder, ", ".join(words)))

    def add_keyword_rule(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить правило по ключевым словам")
        dialog.geometry("400x250")
        dialog.resizable(False, False)

        ttk.Label(dialog, text="Название папки:").pack(pady=(10, 5))
        folder_entry = ttk.Entry(dialog, width=40)
        folder_entry.pack(pady=(0, 10))

        ttk.Label(dialog, text="Ключевые слова (через запятую):").pack(pady=(0, 5))
        keywords_entry = ttk.Entry(dialog, width=40)
        keywords_entry.pack(pady=(0, 10))

        ttk.Label(dialog, text="Пример: отчет, договор, акт", foreground="gray").pack()

        def save():
            folder = folder_entry.get().strip()
            keywords_text = keywords_entry.get().strip()

            if not folder:
                messagebox.showwarning("Предупреждение", "Введите название папки!")
                return

            if not keywords_text:
                messagebox.showwarning("Предупреждение", "Введите хотя бы одно ключевое слово!")
                return

            keywords_list = [kw.strip().lower() for kw in keywords_text.split(',') if kw.strip()]

            if config.add_keyword(folder, keywords_list):
                messagebox.showinfo("Успех", f"Правило для папки '{folder}' добавлено!")
                self.refresh_keywords()
                dialog.destroy()
            else:
                messagebox.showerror("Ошибка", "Не удалось добавить правило!")

        ttk.Button(dialog, text="Сохранить", command=save).pack(pady=10)

    def edit_keyword_rule(self):
        selected = self.keywords_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите правило для редактирования!")
            return

        item = self.keywords_tree.item(selected[0])
        folder_name = item['values'][0]

        keywords_data = config.load_keywords()
        current_keywords = keywords_data.get(folder_name, [])

        dialog = tk.Toplevel(self.root)
        dialog.title(f"Редактировать правило - {folder_name}")
        dialog.geometry("400x250")
        dialog.resizable(False, False)

        ttk.Label(dialog, text=f"Папка: {folder_name}").pack(pady=(10, 5))

        ttk.Label(dialog, text="Ключевые слова (через запятую):").pack(pady=(0, 5))
        keywords_entry = ttk.Entry(dialog, width=40)
        keywords_entry.insert(0, ", ".join(current_keywords))
        keywords_entry.pack(pady=(0, 10))

        ttk.Label(dialog, text="Пример: отчет, договор, акт", foreground="gray").pack()

        def save():
            keywords_text = keywords_entry.get().strip()

            if not keywords_text:
                messagebox.showwarning("Предупреждение", "Введите хотя бы одно ключевое слово!")
                return

            keywords_list = [kw.strip().lower() for kw in keywords_text.split(',') if kw.strip()]

            if config.update_keywords(folder_name, keywords_list):
                messagebox.showinfo("Успех", f"Правило для '{folder_name}' обновлено!")
                self.refresh_keywords()
                dialog.destroy()
            else:
                messagebox.showerror("Ошибка", "Не удалось обновить правило!")

        ttk.Button(dialog, text="Сохранить", command=save).pack(pady=10)

    def delete_keyword_rule(self):
        selected = self.keywords_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите правило для удаления!")
            return

        item = self.keywords_tree.item(selected[0])
        folder_name = item['values'][0]

        if messagebox.askyesno("Подтверждение", f"Удалить правило для папки '{folder_name}'?"):
            if config.remove_keyword_rule(folder_name):
                messagebox.showinfo("Успех", f"Правило для '{folder_name}' удалено!")
                self.refresh_keywords()
            else:
                messagebox.showerror("Ошибка", "Не удалось удалить правило!")

    def clear_all_keywords(self):
        if messagebox.askyesno("Подтверждение", "Удалить ВСЕ правила по ключевым словам?"):
            if config.save_keywords({}):
                messagebox.showinfo("Успех", "Все правила удалены!")
                self.refresh_keywords()
            else:
                messagebox.showerror("Ошибка", "Не удалось удалить правила!")


def main():
    root = tk.Tk()
    app = FileSorterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
