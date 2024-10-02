import json
import os

from src.external_api import get_exchange_rate


def read_transactions_from_json(file_path=None, is_test=False):
    """
    Читает транзакции из JSON-файла.

    Args:
        file_path (str): Путь к файлу с транзакциями. Если не указан, используется стандартный путь.
        is test (bool): Флаг для использования тестовых данных. По умолчанию False.

    Returns:
        list: Список словарей с данными о транзакциях или пустой список при ошибке.

    Raises:
        FileNotFoundError: Если указанный файл не найден.
        ValueError: Если файл не содержит корректных JSON-данных.
    """
    if file_path is None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.join(current_dir, "..")

        if is_test:
            file_path = os.path.join(project_root, "data", "test_operations.json")
        else:
            file_path = os.path.join(project_root, "data", "operations.json")

    # Проверяем, существует ли файл и имеет ли он расширение .json
    if not os.path.exists(file_path) or not file_path.endswith(".json"):
        return []

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
    except Exception as e:
        print(f"Ошибка при чтении файла: {str(e)}")
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
        print(f"Ошибка при получении курсов обмена: {e}")
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
        # Для неизвестных валют используем нулевые значения
        rub_amount = usd_amount = eur_amount = 0.0

    return rub_amount, usd_amount, eur_amount


# Пример использования функции ограниченное демо 10 запросов
operations = read_transactions_from_json()
test_operations = read_transactions_from_json(is_test=True)

# Ограниченный десятью демо-запрос показывающий работоспособность,
# Но не заставляющий ждать вечность подтверждения работоспособности.
for operation in range(10):
    if operation < len(operations):
        rub, usd, eur = transaction_amount(operations[operation])
        print(f"ID: {operations[operation]['id']}")
        print(f"Сумма в рублях: {rub:.2f} RUB")
        print(f"Сумма в долларах: {usd:.2f} USD")
        print(f"Сумма в евро: {eur:.2f} EUR")
        print("---")
    else:
        break
