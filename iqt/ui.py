import tkinter as tk

from iqt.json_handler import JSONHandler
from iqt.cookie_selector import CookieSelector
from iqt.file_selector import FileSelector

from auto_ivan.reader import Reader
from auto_ivan.apishka import mok_send_post_request


class JSONAppUI:
    def __init__(self, root):
        self.root = root
        self.root.title('Автоматизатор3001')
        self.root.geometry('850x600')

        self.json_handler = JSONHandler()
        self.cookie_selector = CookieSelector()
        self.file_selector = FileSelector(on_file_select=self.on_data_file_selected)

        self.main_post_url = '0000'

        self.curr_row = 1
        self.curr_json = None

        self.current_row_label = None
        self.total_rows_label = None
        self.reader = None

        self.create_widgets()

    def create_widgets(self):
        # Сетка для организации элементов
        self.json_output = tk.Text(self.root, wrap=tk.WORD, height=10)
        self.json_output.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Добавляем лейблы для строк
        row_info_frame = tk.Frame(self.root)
        row_info_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nse")

        self.current_row_label = tk.Label(row_info_frame, text="Текущая строка: 1")
        self.current_row_label.pack()

        self.total_rows_label = tk.Label(row_info_frame, text="Всего строк: 0")
        self.total_rows_label.pack()

        self.status_label = tk.Label(row_info_frame, text="Статус: ожидание...")
        self.status_label.pack()

        self.generate_button = tk.Button(self.root, text='Сформировать JSON', command=self.generate_json)
        self.generate_button.grid(row=1, column=0, padx=10, pady=10)

        self.send_button = tk.Button(self.root, text='Отправить JSON', command=self.send_json)
        self.send_button.grid(row=2, column=0, padx=10, pady=10)

        # Секция для куки
        self.cookies_frame = tk.Frame(self.root)
        self.cookies_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

        self.cookies_label = tk.Label(self.cookies_frame, text="Файл cookies: не выбран")
        self.cookies_label.grid(row=0, column=0, padx=10, pady=5)

        self.cookies_button = tk.Button(self.cookies_frame, text='Выбрать файл cookies',
                                        command=self.cookie_selector.select_cookies_file)
        self.cookies_button.grid(row=1, column=0, padx=10, pady=5)

        self.test_button_cookies = tk.Button(self.cookies_frame, text='Тест', command=self.test_cookies_file)
        self.test_button_cookies.grid(row=2, column=0, padx=10, pady=5)

        self.cookies_test_flag = tk.Label(self.cookies_frame, text='Флаг: ожидает файл', fg='grey')
        self.cookies_test_flag.grid(row=3, column=0, padx=10, pady=5)

        # Секция для данных
        ####################################
        self.data_frame = tk.Frame(self.root)
        self.data_frame.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")

        self.data_label = tk.Label(self.data_frame, text="Файл данных: не выбран")
        self.data_label.grid(row=0, column=0, padx=10, pady=5)

        self.data_button = tk.Button(self.data_frame, text='Выбрать файл данных',
                                     command=self.file_selector.select_data_file)
        self.data_button.grid(row=1, column=0, padx=10, pady=5)

        self.test_button_data = tk.Button(self.data_frame, text='Тест', command=self.test_data_file)
        self.test_button_data.grid(row=2, column=0, padx=10, pady=5)

        self.data_test_flag = tk.Label(self.data_frame, text='Флаг: ожидает файл', fg='grey')
        self.data_test_flag.grid(row=3, column=0, padx=10, pady=5)

        # Разделитель между секциями
        self.line1 = tk.Label(self.root, text="-" * 50)
        self.line1.grid(row=5, column=0, padx=10, pady=10, sticky="nsew")

    def test_cookies_file(self):
        # Логика теста для файла cookies
        if self.cookie_selector.cookies_file_path:
            self.cookies_test_flag.config(text="Флаг: пройден", fg="green")
        else:
            self.cookies_test_flag.config(text="Флаг: не пройден", fg="red")

    def test_data_file(self):
        # Логика теста для файла данных
        if self.file_selector.data_file:
            self.data_test_flag.config(text="Флаг: пройден", fg="green")
        else:
            self.data_test_flag.config(text="Флаг: не пройден", fg="red")

    def update_row_info(self):
        if self.reader:
            total_rows = len(self.reader.main_data_sheet.rows)  # Предполагая, что reader.data содержит данные
            self.total_rows_label.config(text=f"Всего строк: {total_rows}")
            self.current_row_label.config(text=f"Текущая строка: {self.curr_row}")

    def on_data_file_selected(self, file_path):
        """Callback, вызываемый после выбора файла в FileSelector"""
        self.reader = Reader(file_path)  # Инициализируем Reader
        self.update_row_info()  # Обновляем информацию о строках

        # Обновляем интерфейс
        self.data_label.config(text=f"Файл данных: {file_path[-20:] if len(file_path) > 20 else file_path}")
        self.data_test_flag.config(text="Флаг: пройден", fg="green")

    def update_status_info(self, status: int | str):
        if status == 200:
            self.status_label.config(text=f"Статус: {status}", fg="green")
        else:
            self.status_label.config(text=f"Статус: {status}", fg="red")

    def send_json(self):
        if self.curr_json and self.cookie_selector.cookies and self.curr_row <= len(self.reader.main_data_sheet.rows):
            s, _, _ = mok_send_post_request(url=self.main_post_url, json_data=self.curr_json,
                                            cookies=self.cookie_selector.cookies)
            if s == 200:
                if self.curr_row < len(self.reader.main_data_sheet.rows):
                    self.curr_row += 1
                    self.update_row_info()
                    self.generate_json()
            self.update_status_info(s)
        else:
            self.update_status_info("Вероятно не хватает какого-то файла")



    def generate_json(self):
        self.curr_json = self.reader.make_json(id_row=self.curr_row)
        self.json_output.delete(1.0, tk.END)
        self.json_output.insert(tk.END, self.curr_json)