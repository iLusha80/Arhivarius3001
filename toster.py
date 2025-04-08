from arhivarius.arhivarius import SimpleXLSXReader
from arhivarius.models import XLSXFile

# === Пример использования ===
if __name__ == "__main__":
    exm_file_name = 'data_2.xlsx'

    reader = SimpleXLSXReader(exm_file_name)
    xlsx_file = XLSXFile(name=exm_file_name, sheets=reader.get_sheets())

    # Вывод информации о файле
    print(f"Файл: {xlsx_file.name}")
    print(f"Количество листов: {len(xlsx_file.sheets)}")

    for sheet in xlsx_file.sheets:
        print(f"Лист: {sheet.name}, строк: {len(sheet.rows)}")

        # Вывод первых 5 строк
        for row in sheet.rows[:5]:
            print(f"Строка {row.id}: {[cell.value for cell in row.cells]}")
            print(f'Типы ячеек: {[cell.type for cell in row.cells]}')

        print('='*88)

        # Вывод первых 5 столбцов
        for col in sheet.columns[:5]:
            print(f"Столбец[{col.name}] {col.id}: {[cell.value for cell in col.cells]}")
