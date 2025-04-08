from PyQt5.QtWidgets import QFileDialog, QMessageBox

class FileSelector:
    def __init__(self, on_file_select=None):
        self.data_file = ''
        self.on_file_select = on_file_select  # Callback-функция

    def select_data_file(self, parent):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getOpenFileName(parent, "Выберите файл данных", "", "All Files (*);;Text Files (*.txt)", options=options)
        if file_path:
            self.data_file = file_path
            self.update_data_label()
            if self.on_file_select:  # Если callback задан - вызываем его
                self.on_file_select(self.data_file)

    def update_data_label(self):
        print(self.data_file)
