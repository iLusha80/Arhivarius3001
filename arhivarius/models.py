from dataclasses import dataclass, field
from typing import List, Optional, Any


@dataclass
class XLSXCell:
    value: Any
    type: str  # 'string', 'number', 'bool', etc.
    address: str  # Например, A1, B2 и т.д.


@dataclass
class XLSXRow:
    id: int  # Номер строки
    cells: List[XLSXCell]


@dataclass
class XLSXColumn:
    id: int  # Номер столбца
    name: Optional[str]  # Имя столбца (если есть заголовок)
    cells: List[XLSXCell]


@dataclass
class XLSXSheet:
    name: str
    rows: List[XLSXRow]
    headers: List[str] = field(init=False)
    columns: List[XLSXColumn] = field(init=False)
    num_columns: int = field(init=False)

    def __post_init__(self):
        if not self.rows:
            self.headers = []
            self.columns = []
            self.num_columns = 0
            return

        # Получаем заголовки из первой строки
        self.headers = [cell.value for cell in self.rows[0].cells]

        # Определяем кол-во столбцов
        self.num_columns = len(self.headers)

        # Формируем столбцы
        self.columns = []
        for col_index in range(self.num_columns):
            col_cells = []
            for row in self.rows[1:]:  # Пропускаем заголовок
                try:
                    col_cells.append(row.cells[col_index])
                except IndexError:
                    col_cells.append(None)
                    print(f"Пропущена ячейка в столбце {col_index} в строке {row.id}")

            column = XLSXColumn(id=col_index, name=self.headers[col_index], cells=col_cells)
            self.columns.append(column)


@dataclass
class XLSXFile:
    name: str
    sheets: List[XLSXSheet]
