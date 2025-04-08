import sys
import json
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel,
                             QPushButton, QVBoxLayout, QHBoxLayout,
                             QTextEdit, QFileDialog, QMessageBox, QFrame)
from PyQt5.QtCore import Qt

from iqt_pyqt.cookie_selector import CookieSelector
from iqt_pyqt.file_selector import FileSelector

from auto_ivan.reader import Reader
from auto_ivan.apishka import mok_send_post_request


class JSONAppUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Автоматизатор3001')
        self.setGeometry(100, 100, 850, 600)

        self.cookie_selector = CookieSelector(self)
        self.file_selector = FileSelector(on_file_select=self.on_data_file_selected)

        self.main_post_url = '0000'

        self.curr_row = 1
        self.curr_json = None

        self.current_row_label = None
        self.total_rows_label = None
        self.reader = None

        self.status_label = None

        self.initUI()

    def initUI(self):
        # Сетка для организации элементов
        main_layout = QVBoxLayout()

        # JSON output
        self.json_output = QTextEdit()
        self.json_output.setReadOnly(True)
        main_layout.addWidget(self.json_output)

        # Row info frame
        row_info_frame = QFrame()
        row_info_layout = QVBoxLayout()
        row_info_frame.setLayout(row_info_layout)

        self.current_row_label = QLabel("Текущая строка: 1")
        row_info_layout.addWidget(self.current_row_label)

        self.total_rows_label = QLabel("Всего строк: 0")
        row_info_layout.addWidget(self.total_rows_label)

        self.status_label = QLabel("Статус: ожидание...")
        row_info_layout.addWidget(self.status_label)

        # Layout for JSON output and row info
        json_row_layout = QHBoxLayout()
        json_row_layout.addWidget(self.json_output)
        json_row_layout.addWidget(row_info_frame)
        main_layout.addLayout(json_row_layout)

        # Buttons
        self.generate_button = QPushButton('Сформировать JSON')
        self.generate_button.clicked.connect(self.generate_json)
        main_layout.addWidget(self.generate_button)

        self.send_button = QPushButton('Отправить JSON')
        self.send_button.clicked.connect(self.send_json)
        main_layout.addWidget(self.send_button)

        # Cookies section
        self.cookies_frame = QFrame()
        cookies_layout = QVBoxLayout()
        self.cookies_frame.setLayout(cookies_layout)

        self.cookies_label = QLabel("Файл cookies: не выбран")
        cookies_layout.addWidget(self.cookies_label)

        self.cookies_button = QPushButton('Выбрать файл cookies')
        self.cookies_button.clicked.connect(lambda: self.cookie_selector.select_cookies_file(self))
        cookies_layout.addWidget(self.cookies_button)

        self.test_button_cookies = QPushButton('Тест')
        self.test_button_cookies.clicked.connect(self.test_cookies_file)
        cookies_layout.addWidget(self.test_button_cookies)

        self.cookies_test_flag = QLabel('Флаг: ожидает файл')
        self.cookies_test_flag.setStyleSheet("color: grey;")
        cookies_layout.addWidget(self.cookies_test_flag)
        main_layout.addWidget(self.cookies_frame)

        # Data section
        self.data_frame = QFrame()
        data_layout = QVBoxLayout()
        self.data_frame.setLayout(data_layout)

        self.data_label = QLabel("Файл данных: не выбран")
        data_layout.addWidget(self.data_label)

        self.data_button = QPushButton('Выбрать файл данных')
        self.data_button.clicked.connect(lambda: self.file_selector.select_data_file(self))
        data_layout.addWidget(self.data_button)

        self.test_button_data = QPushButton('Тест')
        self.test_button_data.clicked.connect(self.test_data_file)
        data_layout.addWidget(self.test_button_data)

        self.data_test_flag = QLabel('Флаг: ожидает файл')
        self.data_test_flag.setStyleSheet("color: grey;")
        data_layout.addWidget(self.data_test_flag)
        main_layout.addWidget(self.data_frame)

        # Separator
        line1 = QFrame()
        line1.setFrameShape(QFrame.HLine)
        line1.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(line1)

        self.setLayout(main_layout)

    def test_cookies_file(self):
        # Логика теста для файла cookies
        if self.cookie_selector.cookies_file_path:
            self.cookies_test_flag.setText("Флаг: пройден")
            self.cookies_test_flag.setStyleSheet("color: green;")
        else:
            self.cookies_test_flag.setText("Флаг: не пройден")
            self.cookies_test_flag.setStyleSheet("color: red;")

    def test_data_file(self):
        # Логика теста для файла данных
        if self.file_selector.data_file:
            self.data_test_flag.setText("Флаг: пройден")
            self.data_test_flag.setStyleSheet("color: green;")
        else:
            self.data_test_flag.setText("Флаг: не пройден")
            self.data_test_flag.setStyleSheet("color: red;")

    def update_row_info(self):
        if self.reader:
            total_rows = len(self.reader.main_data_sheet.rows)  # Предполагая, что reader.data содержит данные
            self.total_rows_label.setText(f"Всего строк: {total_rows}")
            self.current_row_label.setText(f"Текущая строка: {self.curr_row}")

    def on_data_file_selected(self, file_path):
        """Callback, вызываемый после выбора файла в FileSelector"""
        self.reader = Reader(file_path)  # Инициализируем Reader
        self.update_row_info()  # Обновляем информацию о строках

        # Обновляем интерфейс
        self.data_label.setText(f"Файл данных: {file_path[-20:] if len(file_path) > 20 else file_path}")
        self.data_test_flag.setText("Флаг: пройден")
        self.data_test_flag.setStyleSheet("color: green;")

    def update_status_info(self, status: int | str):
        if status == 200:
            self.status_label.setText(f"Статус: {status}")
            self.status_label.setStyleSheet("color: green;")
        else:
            self.status_label.setText(f"Статус: {status}")
            self.status_label.setStyleSheet("color: red;")

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
        self.json_output.clear()
        self.json_output.insertPlainText(json.dumps(self.curr_json, indent=4))