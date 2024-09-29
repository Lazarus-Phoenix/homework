import os
import json


def read_transactions_from_json():
    """
    Читает JSON-файл из директории data в корне проекта и возвращает список словарей с данными о финансовых транзакциях.

    Returns:
        list: Список словарей с данными о финансовых транзакциях.
        Если файл пустой, содержит не список или не найден, возвращает пустой список.
    """

    # Определяем путь к файлу относительно текущего скрипта
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(current_dir, '..')
    file_path = os.path.join(project_root, 'data', 'operations.json')

    # Проверяем, существует ли файл и имеет ли он расширение .json
    if not os.path.exists(file_path) or not file_path.endswith('.json'):
        return []
    else:
        try:
            with open(file_path) as f:
                data = json.load(f)

            # Проверяем, является ли загруженное значение списком
            if isinstance(data, list):
                return data
            else:
                return []
        except json.JSONDecodeError:
            # Если произошла ошибка при декодировании JSON, возвращаем пустой список
            return []


# В корне проекта или из любой другой части проекта
operations = read_transactions_from_json()
print(operations)