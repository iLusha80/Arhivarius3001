from PyQt5.QtWidgets import QFileDialog, QMessageBox

class CookieSelector:
    def __init__(self, ui):
        self.ui = ui
        self.cookies_file_path = ''
        self.cookies = {}

    def select_cookies_file(self, parent):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getOpenFileName(parent, "Выберите файл cookies", "", "All Files (*);;Text Files (*.txt)", options=options)
        if file_path:
            self.cookies_file_path = file_path
            self.update_cookies_label()
            self.cookies = self.load_cookies()

    def update_cookies_label(self):
        if self.cookies_file_path:
            self.ui.cookies_label.setText(f"Файл cookies: {self.cookies_file_path}")
        else:
            self.ui.cookies_label.setText("Файл cookies: не выбран")

    def load_cookies(self) -> dict:
        """
        Загрузка Печенек в переменную
        """
        cookies = {}

        try:
            with open(self.cookies_file_path, 'r') as file:
                data = file.read()
            lst = data.split(';')
            for line in lst:
                if line:
                    key, value = line.strip().split('=')
                    cookies[key] = value
            return cookies
        except Exception as e:
            QMessageBox.critical(None, "Ошибка", f"Ошибка при загрузке файла cookies: {e}")
            return {}