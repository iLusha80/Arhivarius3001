import requests


def fetch_kp_id(cookies: dict, code_kp: str = 'П1543') -> int | None:
    """
    Args:
        cookies (dict): Словарь печенек
        code_kp (str): Строковое название процесса "П1543"

    Returns:
        int | None: Возвращает id процесса из API запроса.
                    None в случае ошибки или отсутствия code_kp
    """
    url_tmp = f'https://dbpm.sberbank.ru/api/dictionary-service/v1.1/internal/process?code={code_kp}'

    response = requests.get(url_tmp, cookies=cookies, verify=False)
    if response.status_code == 200:
        try:
            data = response.json()
            res_id = data.get('id', 'Поле id не найдено')
            print(f'ID = {res_id} ({code_kp})')
            return res_id
        except Exception as e:
            print(f'Ошибка получения id процесса\n', str(e))
            return None
    else:
        print(f'Ошибка запроса. Статус код - {response.status_code}')
        return None


def send_post_request(url, json_data=None, cookies=None):
    """Отправляет POST запрос с JSON данными и куками.

    Args:
        url (str): URL для запроса
        json_data (dict, optional): Данные для отправки в формате JSON. Defaults to None.
        cookies (dict, optional): Словарь с куками в формате {name: value}. Defaults to None.

    Returns:
        tuple: Кортеж содержащий:
            - status_code (int): HTTP статус-код ответа
            - response_data (dict): Ответ сервера в виде словаря
            - response_cookies (dict): Куки из ответа сервера {name: value}

    Examples:
        >>> status, data, cookies = send_post_request(
        ...     "https://api.example.com/login",
        ...     json_data={"user": "admin", "password": "secret"},
        ...     cookies={"session": "123"}
        ... )
    """
    try:
        response = requests.post(
            url,
            json=json_data or {},
            cookies=cookies or {}
        )
        response.raise_for_status()
        return (
            response.status_code,
            response.json(),
            dict(response.cookies)
        )
    except requests.exceptions.RequestException as e:
        return (
            getattr(e.response, 'status_code', None),
            {'error': str(e)},
            {}
        )

def mok_fetch_kp_id(cookies: dict, code_kp: str = 'П1543') -> int | None:
    return 709

def mok_send_post_request(url, json_data=None, cookies=None):
    return 200, {}, {}