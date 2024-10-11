import os
from typing import List, Dict, Any

import pandas as pd


def read_csv(file_path: str = "operations.csv") -> List[Dict[str, Any]]:
    """
    Читает финансовые операции из CSV-файла.

    Args:
    file_path (str): Путь к CSV-файлу.

    Returns:
    List[Dict]: Список словарей с данными о финансовых операциях.
    """
    try:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.join(project_root, "data")
        full_path = os.path.join(data_dir, file_path)

        df = pd.read_csv(full_path, delimiter=';')

        # Преобразуем DataFrame в список словарей
        data = df.to_dict("records")
        
        # Обновляем структуру данных для соответствия ожидаемому формату
        updated_data = []
        for item in data:
            updated_item = {
                "id": item.get("id", ""),
                "state": item.get("state", ""),
                "date": item.get("date", ""),
                "operationAmount": {
                    "amount": item.get("amount", "0"),
                    "currency": {
                        "code": item.get("currency_code", "")
                    }
                },
                "description": item.get("description", ""),
                "from": item.get("from", ""),
                "to": item.get("to", "")
            }
            updated_data.append(updated_item)
        

        return updated_data
    except Exception as e:
        print(f"Ошибка при чтении CSV-файла: {str(e)}")
        return []
