import os
from typing import Any, Dict, List

import pandas as pd


def read_xlsx(file_path: str = "operations.xlsx") -> List[Dict[str, Any]]:
    """
    Читает данные из XLSX-файла.
    """
    try:
        # Получаем путь к корневой директории проекта
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.join(project_root, "data")
        full_path = os.path.join(data_dir, file_path)

        df = pd.read_excel(full_path)

        # Преобразуем DataFrame в список словарей
        data = df.to_dict("records")

        # Обновляем структуру данных для соответствия ожидаемому формату
        updated_data = []
        for item in data:
            currency_code = item.get("currency_code", "RUB")  # Берем валюту из колонки F, если нет - по умолчанию RUB
            updated_item = {
                "id": item.get("id", ""),
                "state": item.get("state", ""),
                "date": item.get("date", ""),
                "operationAmount": {
                    "amount": str(item.get("amount", "0")),  # Преобразуем в строку
                    "currency": {"code": currency_code},
                },
                "description": item.get("description", ""),
                "from": item.get("from", ""),
                "to": item.get("to", ""),
            }
            updated_data.append(updated_item)

        return updated_data

    except FileNotFoundError:
        print(f"Файл {full_path} не найден")
        return []

    except Exception as e:
        print(f"Ошибка при чтении файла {full_path}: {e}")
        return []
