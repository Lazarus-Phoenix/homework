import json
import os

from typing import List, Dict, Any

from src.external_api import get_exchange_rate

import logging

# Создаем корневой logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Создаем файловый хендлер
file_handler = logging.FileHandler('logs/log_utils.log')
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)


def read_transactions_from_json(file_path: str = None, is_test: bool = False) -> List[Dict[str, Any]]:
    """
    Читает транзакции из JSON-файла.
    """
    logger.info(f"Начало чтения транзакций из файла {file_path}")

    if file_path is None:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.join(project_root, "data")

        if is_test:
            file_path = os.path.join(data_dir, "test_operations.json")
        else:
            file_path = os.path.join(data_dir, "operations.json")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if isinstance(data, list):
            logger.info(f"Успешно прочитано {len(data)} операций.")
            return data
        else:
            logger.error("Данные в файле не являются списком")
            return []

    except FileNotFoundError:
        logger.error(f"Файл {file_path} не найден")
        return []

    except json.JSONDecodeError:
        logger.error(f"Ошибка при декодировании JSON в файле {file_path}")
        return []

    except Exception as e:
        logger.exception(f"Ошибка при чтении файла {file_path}: {e}")
        return []


# Использование функции
# Для стандартного файла
standard_ops = read_transactions_from_json()
# Для тестового файла
test_ops = read_transactions_from_json(is_test=True)


def transaction_amount(transaction):
    """
    Вычисляет сумму транзакции в рублях, долларах и евро.

    Args:
        transaction (dict): Словарь с данными о транзакции.

    Returns:
        tuple: Кортеж из трех float значений - сумма в рублях, долларах и евро соответственно.

    Raises:
        ValueError: При некорректных данных транзакции.
    """
    # Получаем сумму и валюту из транзакции
    amount_str = transaction["operationAmount"]["amount"]
    currency_code = transaction["operationAmount"]["currency"]["code"]

    # Конвертируем сумму из строки в float
    amount = float(amount_str.replace(",", "."))

    # Получаем актуальные курсы обмена
    try:
        usd_to_rub = float(get_exchange_rate("USD"))
        eur_to_rub = float(get_exchange_rate("EUR"))
    except Exception as e:
        # Используем запасные значения, если не удалось получить актуальные курсы
        usd_to_rub = 60.0
        eur_to_rub = 65.0

    # Вычисляем суммы в разных валютах
    if currency_code == "RUB":
        rub_amount = amount
        usd_amount = amount / usd_to_rub
        eur_amount = amount / eur_to_rub
    elif currency_code == "USD":
        rub_amount = amount * usd_to_rub
        usd_amount = amount
        eur_amount = amount * usd_to_rub / eur_to_rub
    elif currency_code == "EUR":
        rub_amount = amount * eur_to_rub
        usd_amount = amount * eur_to_rub / usd_to_rub
        eur_amount = amount
    else:
        # Для неизв��стных валют используем нулевые значения
        rub_amount = usd_amount = eur_amount = 0.0
    return rub_amount, usd_amount, eur_amount


# Пример использования функции ограниченное демо 10 запросов
operations = read_transactions_from_json()
test_operations = read_transactions_from_json(is_test=True)

