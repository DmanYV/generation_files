import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import re


class FileGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор файлов")

        self.extensions = [
            "txt", "doc", "docx", "pdf", "xls", "xlsx", "jpg", "jpeg",
            "png", "gif", "mp3", "mp4", "avi", "mov", "zip", "rar",
            "7z", "exe", "dll", "py", "java", "html", "css", "js",
            "json", "xml", "csv", "ppt", "pptx", "sql"
        ]
        self.units = ["мегабайты", "килобайты", "байты"]

        self.create_widgets()

    def validate_number(self, new_value):
        """Проверка ввода: максимум 2 знака после точки"""
        return re.fullmatch(r'^\d*\.?\d{0,2}$', new_value) is not None

    def create_widgets(self):
        # Название файла
        ttk.Label(self.root, text="Название файла:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.filename_entry = ttk.Entry(self.root)
        self.filename_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=2, sticky="ew")

        # Расширение файла
        ttk.Label(self.root, text="Расширение файла:").grid(row=2, column=0, padx=5, pady=2, sticky="w")
        self.extension_combobox = ttk.Combobox(self.root, values=self.extensions, state="readonly")
        self.extension_combobox.grid(row=3, column=0, columnspan=2, padx=5, pady=2, sticky="ew")

        # Размер файла и единицы измерения
        ttk.Label(self.root, text="Размер файла:").grid(row=4, column=0, padx=5, pady=2, sticky="w")

        frame = ttk.Frame(self.root)
        frame.grid(row=5, column=0, columnspan=2, padx=5, pady=2, sticky="ew")

        validate_cmd = self.root.register(self.validate_number)
        self.size_entry = ttk.Entry(frame, validate="key", validatecommand=(validate_cmd, '%P'))
        self.size_entry.pack(side="left", fill="x", expand=True)

        self.unit_combobox = ttk.Combobox(frame, values=self.units, width=10, state="readonly")
        self.unit_combobox.pack(side="left", padx=5)
        self.unit_combobox.set(self.units[0])  # Установка мегабайтов по умолчанию

        # Кнопка генерации
        self.generate_button = ttk.Button(self.root, text="Генерировать", command=self.generate_file)
        self.generate_button.grid(row=6, column=0, columnspan=2, padx=5, pady=10, sticky="ew")

        self.root.columnconfigure(0, weight=1)

    def generate_file(self):
        """Генерация файла по заданным параметрам"""
        filename = self.filename_entry.get().strip()
        extension = self.extension_combobox.get().strip()
        size_text = self.size_entry.get().strip()
        unit = self.unit_combobox.get().strip()

        # Проверка заполнения полей
        if not all([filename, extension, size_text, unit]):
            messagebox.showerror("Ошибка", "Заполните все поля")
            return

        # Преобразование размера
        try:
            size = float(size_text)
            if size <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректный размер файла")
            return

        # Конвертация в байты
        if unit == "мегабайты":
            size_bytes = size * 1024 * 1024
        elif unit == "килобайты":
            size_bytes = size * 1024
        else:  # байты
            size_bytes = size
        size_bytes = int(round(size_bytes))

        # Диалог сохранения файла
        default_name = f"{filename}.{extension}"
        filepath = filedialog.asksaveasfilename(
            defaultextension=f".{extension}",
            initialfile=default_name,
            filetypes=[(f"{extension.upper()} файлы", f"*.{extension}"), ("Все файлы", "*.*")]
        )

        if not filepath:
            return  # Отмена сохранения

        # Создание файла
        try:
            with open(filepath, 'wb') as f:
                f.seek(size_bytes - 1)
                f.write(b'\0')
            messagebox.showinfo("Успех", f"Файл успешно создан:\n{filepath}\nРазмер: {size_bytes} байт")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка создания файла:\n{str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = FileGeneratorApp(root)
    root.mainloop()