from arhivarius.arhivarius import SimpleXLSXReader
from arhivarius.models import XLSXFile, XLSXRow, XLSXSheet
from auto_ivan.apishka import fetch_kp_id, mok_fetch_kp_id

class Reader:
    def __init__(self, filename: str):
        self.filename = filename
        self.main_data_sheet: XLSXSheet = self._get_data_sheet(self.filename)

    def _get_data_sheet(self, exm_file_name: str) -> XLSXSheet:
        reader = SimpleXLSXReader(exm_file_name)
        xlsx_file = XLSXFile(name=exm_file_name, sheets=reader.get_sheets())
        return xlsx_file.sheets[0]

    def make_json(self, id_row: int, coockies : dict) -> dict:
        code_kp = self.main_data_sheet.rows[id_row].cells[0].value
        id_kp = fetch_kp_id(cookies=coockies, code_kp=code_kp)

        bus_desc_url = self.main_data_sheet.rows[id_row].cells[1].value
        try:
            employee_number_alone = str(int(self.main_data_sheet.rows[id_row].cells[3].value))
        except:
            employee_number_alone = "0"

        tmp_employee_number_row = self.main_data_sheet.rows[id_row].cells[4].value

        employee_number_list = list()
        employee_number_list.append(employee_number_alone)
        employee_number_list.extend(self._get_employee_numbers(tmp_employee_number_row))

        employee_number_set = set(employee_number_list)

        json_data = {
            "assignees": [{"employeeNumber": num} for num in employee_number_set],
            "taskType": "TASK_BUS_DESC_CHECKBOX",
            "busDescCheckboxTaskRequest": {
                "processId": id_kp,
                "busDescUrl": bus_desc_url
            }
        }
        return json_data

    def _get_employee_numbers(self, tmp_employee_number_row: str) -> list:
        """
        Берет строку, разбивает ее на список, берет каждый элемент списка,
        разбивает его на 2 части, берет вторую, конвертирует в int и добавляет
        в результат
        Args:
            tmp_employee_number_row (str): строка, которую нужно разбить

        Returns:
            list: список employee_number
        """
        lst_data = tmp_employee_number_row.split(';')
        result = list()
        for data in lst_data:
            curr_empl = str(int(data.split('_')[1]))
            result.append(curr_empl)
        return result

