from tkinter import filedialog

class FileSelector:
    def __init__(self, on_file_select=None):
        self.data_file = ''
        self.on_file_select = on_file_select  # Callback-функция

    def select_data_file(self):
        self.data_file = filedialog.askopenfilename(title="Выберите файл данных")
        if self.data_file:
            self.update_data_label()
            if self.on_file_select:  # Если callback задан - вызываем его
                self.on_file_select(self.data_file)

    def update_data_label(self):
        print(self.data_file)