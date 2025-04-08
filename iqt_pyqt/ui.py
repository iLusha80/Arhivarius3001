import sys
import json
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel,
                             QPushButton, QVBoxLayout, QHBoxLayout,
                             QTextEdit, QFileDialog, QMessageBox, QFrame, QGridLayout)
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
        main_layout = QGridLayout()

        # JSON output
        self.json_output = QTextEdit()
        self.json_output.setReadOnly(True)
        # main_layout.addWidget(self.json_output) # Will be added to grid later

        self.current_row_label = QLabel("Текущая строка: 1")

        self.total_rows_label = QLabel("Всего строк: 0")

        self.status_label = QLabel("Статус: ожидание...")


        # Buttons
        self.generate_button = QPushButton('Сформировать JSON')
        self.generate_button.clicked.connect(self.generate_json)
        # main_layout.addWidget(self.generate_button) # Will be added to grid later

        self.send_button = QPushButton('Отправить JSON')
        self.send_button.clicked.connect(self.send_json)
        # main_layout.addWidget(self.send_button) # Will be added to grid later

        # Cookies section

        self.cookies_label = QLabel("Файл cookies: не выбран")
        self.cookies_label.setStyleSheet("background-color: #f0f0f0; border: 1px solid #ccc; padding: 5px;")

        self.cookies_button = QPushButton('Выбрать файл cookies')
        self.cookies_button.setStyleSheet("background-color: #e0e0e0; border: 1px solid #bbb; padding: 5px;")
        self.cookies_button.clicked.connect(lambda: self.cookie_selector.select_cookies_file(self))

        self.test_button_cookies = QPushButton('Тест')
        self.test_button_cookies.setStyleSheet("background-color: #e0e0e0; border: 1px solid #bbb; padding: 5px;")
        self.test_button_cookies.clicked.connect(self.test_cookies_file)

        self.cookies_test_flag = QLabel('Флаг: ожидает файл')
        self.cookies_test_flag.setStyleSheet("color: grey; background-color: #f0f0f0; border: 1px solid #ccc; padding: 5px;")
        # main_layout.addWidget(self.cookies_frame) # Will be added to grid later

        # Data section

        self.data_label = QLabel("Файл данных: не выбран")
        self.data_label.setStyleSheet("background-color: #f0f0f0; border: 1px solid #ccc; padding: 5px;")

        self.data_button = QPushButton('Выбрать файл данных')
        self.data_button.setStyleSheet("background-color: #e0e0e0; border: 1px solid #bbb; padding: 5px;")
        self.data_button.clicked.connect(lambda: self.file_selector.select_data_file(self))

        self.test_button_data = QPushButton('Тест')
        self.test_button_data.setStyleSheet("background-color: #e0e0e0; border: 1px solid #bbb; padding: 5px;")
        self.test_button_data.clicked.connect(self.test_data_file)

        self.data_test_flag = QLabel('Флаг: ожидает файл')
        self.data_test_flag.setStyleSheet("color: grey; background-color: #f0f0f0; border: 1px solid #ccc; padding: 5px;")
        # main_layout.addWidget(self.data_frame) # Will be added to grid later

        # Separator
        line1 = QFrame()
        line1.setFrameShape(QFrame.HLine)
        line1.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(line1)

        self.setLayout(main_layout)

        # Add widgets to grid layout
        main_layout.addWidget(self.json_output, 0, 0, 1, 4) # row, col, rowspan, colspan
        main_layout.addWidget(self.current_row_label, 1, 0)
        main_layout.addWidget(self.total_rows_label, 1, 1)
        main_layout.addWidget(self.status_label, 1, 2)
        main_layout.addWidget(self.generate_button, 2, 0)
        main_layout.addWidget(self.send_button, 2, 1)

        main_layout.addWidget(self.cookies_label, 3, 0)
        main_layout.addWidget(self.cookies_button, 3, 1)
        main_layout.addWidget(self.test_button_cookies, 3, 2)
        main_layout.addWidget(self.cookies_test_flag, 3, 3)

        main_layout.addWidget(self.data_label, 4, 0)
        main_layout.addWidget(self.data_button, 4, 1)
        main_layout.addWidget(self.test_button_data, 4, 2)
        main_layout.addWidget(self.data_test_flag, 4, 3)

        main_layout.setColumnStretch(0, 3) # json_output column
        main_layout.setColumnStretch(1, 1)
        main_layout.setColumnStretch(2, 1)
        main_layout.setColumnStretch(3, 1)

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