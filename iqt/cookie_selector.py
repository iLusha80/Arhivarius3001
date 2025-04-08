from tkinter import filedialog

class CookieSelector:
    def __init__(self):
        self.cookies_file_path = ''
        self.cookies = {}

    def select_cookies_file(self):
        self.cookies_file_path = filedialog.askopenfilename(title="Выберите файл cookies")
        if self.cookies_file_path:
            self.cookies = self.load_cookies()

    def load_cookies(self) -> dict:
        """
        Загрузка Печенек в переменную
        """
        cookies = {}

        with open(self.cookies_file_path, 'r') as file:
            data = file.read()
        lst = data.split(';')
        for line in lst:
            if line:
                key, value = line.strip().split('=')
                cookies[key] = value
        return cookies
