# json_handler.py
import json

class JSONHandler:
    def generate_json(self, cookies_text, data_text):
        json_data = {
            'cookies': cookies_text,
            'data_file': data_text
        }
        return json.dumps(json_data, ensure_ascii=False, indent=4)
