import tkinter as tk
from tkinter import filedialog
import json

class JSONApp:
    def __init__(self, root):
        self.root = root
        self.root.title('JSON Builder')
        self.root.geometry('800x600')

        # Поле для отображения JSON
        self.json_output = tk.Text(root, wrap=tk.WORD, height=10, font=("Arial", 20))
        self.json_output.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

        # Кнопка для формирования JSON
        self.generate_button = tk.Button(root, text='Сформировать JSON', command=self.generate_json)
        self.generate_button.pack(pady=10)

        # Кнопка для отправки JSON
        self.send_button = tk.Button(root, text='Отправить JSON')
        self.send_button.pack(pady=10)

        # Элементы для выбора файлов cookies и data
        self.cookies_button = tk.Button(root, text='Выбрать файл cookies', command=self.select_cookies_file)
        self.cookies_button.pack(pady=5)

        self.data_button = tk.Button(root, text='Выбрать файл данных', command=self.select_data_file)
        self.data_button.pack(pady=5)

        # Отображение выбранных файлов
        self.cookies_label = tk.Label(root, text='Файл cookies: не выбран')
        self.cookies_label.pack(pady=5)

        self.data_label = tk.Label(root, text='Файл данных: не выбран')
        self.data_label.pack(pady=5)

    def generate_json(self):
        # Пример генерации JSON (для теста можно добавить больше полей)
        json_data = {
            'cookies': self.cookies_label.cget("text"),
            'data_file': self.data_label.cget("text")
        }
        self.json_output.delete(1.0, tk.END)  # Очищаем поле вывода
        self.json_output.insert(tk.END, json.dumps(json_data, ensure_ascii=False, indent=4))

    def select_cookies_file(self):
        file_name = filedialog.askopenfilename(title="Выберите файл cookies")
        if file_name:
            self.cookies_label.config(text=f'Файл cookies: {file_name}')

    def select_data_file(self):
        file_name = filedialog.askopenfilename(title="Выберите файл данных")
        if file_name:
            self.data_label.config(text=f'Файл данных: {file_name}')

