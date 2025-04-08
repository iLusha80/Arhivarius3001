import os
from pathlib import Path

class PyFilesCollector:
    IGNORE_DIRS = {'venv', '__pycache__', '.git', '.venv'}  # Папки для игнорирования

    @classmethod
    def collect_py_files(cls, root_dir, output_file):
        """Собирает все .py файлы, игнорируя указанные папки"""
        with open(output_file, 'w', encoding='utf-8') as out_f:
            for py_file in Path(root_dir).rglob('*.py'):
                if any(ignore in py_file.parts for ignore in cls.IGNORE_DIRS):
                    continue
                out_f.write(f"\n\n***[file] {py_file}***\n\n")
                out_f.write(Path(py_file).read_text(encoding='utf-8'))

    @classmethod
    def restore_py_files(cls, input_file):
        """Восстанавливает файлы из собранного файла"""
        with open(input_file, 'r', encoding='utf-8') as f:
            current_file, content = None, []
            for line in f:
                if line.startswith('***[file]') and line.endswith('***\n'):
                    if current_file: cls._save_file(current_file, content)
                    current_file, content = Path(line[10:-4].strip()), []
                else: content.append(line)
            if current_file: cls._save_file(current_file, content)

    @staticmethod
    def _save_file(path, content):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(''.join(content), encoding='utf-8')

# Пример использования:
if __name__ == "__main__":
    collector = PyFilesCollector()

    # Собрать все .py файлы из текущей директории в all_py_files.txt
    collector.collect_py_files('.', 'all_py_files.txt')

    # Восстановить файлы из all_py_files.txt
    # collector.restore_py_files('all_py_files.txt')