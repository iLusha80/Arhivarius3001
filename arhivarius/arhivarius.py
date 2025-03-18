import zipfile
import xml.etree.ElementTree as ET

from arhivarius.models import XLSXFile, XLSXCell, XLSXRow, XLSXSheet


class SimpleXLSXReader:
    def __init__(self, filename: str):
        self.filename = filename
        self.shared_strings = []
        self.sheets = []
        self._parse_xlsx()

    def _parse_xlsx(self):
        """Читает xlsx-файл как ZIP-архив и парсит данные."""
        with zipfile.ZipFile(self.filename, 'r') as z:
            # 1. Загружаем sharedStrings.xml (хранит строки)
            if 'xl/sharedStrings.xml' in z.namelist():
                with z.open('xl/sharedStrings.xml') as f:
                    tree = ET.parse(f)
                    root = tree.getroot()
                    self.shared_strings = [
                        t.text for t in root.findall('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t')
                    ]

            # 2. Читаем workbook.xml (получаем названия листов)
            sheet_names = {}
            with z.open("xl/workbook.xml") as f:
                tree = ET.parse(f)
                root = tree.getroot()
                ns = {"ns": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
                sheets = root.findall("ns:sheets/ns:sheet", ns)

                for sheet in sheets:
                    sheet_id = sheet.attrib["sheetId"]
                    sheet_names[sheet_id] = sheet.attrib["name"]

            # 3. Загружаем все листы
            for sheet_id, sheet_name in sheet_names.items():
                sheet_data = self._parse_sheet(z, sheet_id)
                self.sheets.append(XLSXSheet(name=sheet_name, rows=sheet_data))

    def _parse_sheet(self, z: zipfile.ZipFile, sheet_id: str):
        """Парсит отдельный лист и возвращает список строк (XLSXRow)."""
        sheet_path = f"xl/worksheets/sheet{sheet_id}.xml"
        if sheet_path not in z.namelist():
            return []

        with z.open(sheet_path) as f:
            tree = ET.parse(f)
            root = tree.getroot()
            ns = {"ns": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}

            rows = []
            for row in root.findall("ns:sheetData/ns:row", ns):
                row_id = int(row.attrib["r"])
                cells = []

                for cell in row.findall("ns:c", ns):
                    cell_address = cell.attrib["r"]  # Например, "A1"
                    cell_type = cell.get("t", "n")  # Тип: 's' - строка, иначе число
                    value_element = cell.find("ns:v", ns)

                    if value_element is not None:
                        value = value_element.text
                        if cell_type == "s":  # Если строка, то берем из sharedStrings
                            value = self.shared_strings[int(value)]
                    else:
                        value = ""

                    cells.append(XLSXCell(value=value, type=cell_type, address=cell_address))

                rows.append(XLSXRow(id=row_id, cells=cells))

            return rows

    def get_sheets(self):
        """Возвращает список всех листов."""
        return self.sheets

    def get_sheet_by_name(self, name: str):
        """Возвращает лист по имени."""
        for sheet in self.sheets:
            if sheet.name == name:
                return sheet
        return None
