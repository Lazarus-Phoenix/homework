import pandas as pd
import os
from typing import List, Dict


def read_csv(file_path: str) -> List[Dict]:
    """
    Читает финансовые операции из CSV-файла.

    Args:
    file_path (str): Путь к CSV-файлу.

    Returns:
    List[Dict]: Список словарей с данными о финансовых операциях.
    """
    try:
        df = pd.read_csv(file_path)
        return df.to_dict('records')
    except Exception as e:
        print(f"Ошибка при чтении CSV-файла: {str(e)}")
        return []


def read_xlsx(file_path: str) -> List[Dict]:
    """
    Читает финансовые операции из XLSX-файла.

    Args:
    file_path (str): Путь к XLSX-файлу.

    Returns:
    List[Dict]: Список словарей с данными о финансовых операциях.
    """
    try:
        df = pd.read_excel(file_path)
        return df.to_dict('records')
    except Exception as e:
        print(f"Ошибка при чтении XLSX-файла: {str(e)}")
        return []


def read_all_files_in_directory(directory: str) -> List[Dict]:
    """
    Читает все файлы CSV и XLSX в указанной директории.

    Args:
    directory (str): Путь к директории с файлами.

    Returns:
    List[Dict]: Объединенный список словарей с данными о финансовых операциях из всех файлов.
    """
    all_data = []
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if filename.endswith('.csv'):
            all_data.extend(read_csv(file_path))
        elif filename.endswith('.xlsx'):
            all_data.extend(read_xlsx(file_path))
    return all_data


# Пример использования
if __name__ == "__main__":
    # Получаем абсолютный путь к директории проекта
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_directory = os.path.join(project_root, "data")

    print(f"Путь к директории с данными: {data_directory}")

    if os.path.exists(data_directory):
        all_operations = read_all_files_in_directory(data_directory)
        print(f"Общее количество операций: {len(all_operations)}")
        if all_operations:
            print("Пример первой операции:")
            print(all_operations[0])
    else:
        print(
            "Директория с данными не найдена. Пожалуйста, убедитесь, что директория 'data' существует в корне проекта.")