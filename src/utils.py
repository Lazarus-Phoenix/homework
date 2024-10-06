import logging
import os
import json
from src.external_api import get_exchange_rate

# Получаем путь к корневой директории проекта
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Создаем директорию для логов в корне проекта, если она не существует
log_dir = os.path.join(project_root, 'logs')
os.makedirs(log_dir, exist_ok=True)

# Получаем логгер для модуля utils
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Создаем файловый обработчик
file_handler = logging.FileHandler(os.path.join(log_dir, 'log_utils.log'))
file_handler.setLevel(logging.DEBUG)

# Создаем консольный обработчик для проверки на серьёзные проблемы в работе кода.
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.ERROR)

# Создае�� форматтер
formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')

# Добавляем форматтер к обработчикам
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Добавляем обработчики к логгеру
logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.debug('Debug message')


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
    logger.debug(f"Вызван read_transactions_from_json с аргументами: file_path={file_path}, is_test={is_test}")

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
        logger.info(f"Попытка чтения файла: {file_path}")

    try:
        with open(file_path) as f:
            data = json.load(f)

        # Проверяем, является ли загруженное значение списком
        if isinstance(data, list):
            logger.info(f"Успешно прочитано {len(data)} транзакций")
            return data
        else:
            logger.warning("Данные в файле не являются списком")
            return []

    except json.JSONDecodeError:
        logger.debug(f"Ошибка при декодировании JSON в файле {file_path}")
        return []

    except Exception as e:
        logger.debug(f"Ошибка при чтении файла {file_path}: {str(e)}")
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
    logger.debug(f"Вызван transaction_amount с аргументом: {transaction}")
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
        logger.error(f"Ошибка при получении курсов обмена: {e}")
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
        logger.error(f" Неизвестная валюта : {str(e)}")
    return rub_amount, usd_amount, eur_amount
    logger.info(f"Вычислена сумма транзакции: {amount} {currency_code}")


# Пример использования функции ограниченное демо 10 запросов
operations = read_transactions_from_json()
test_operations = read_transactions_from_json(is_test=True)

# Ограниченный десятью демо-запрос показывающий работоспособность,
# Но не заставляющий ждать вечность подтверждения работоспособности.
for operation in range(10):
    if operation < len(operations):
        logger.info("Запуск примера использования функций utils")
        rub, usd, eur = transaction_amount(operations[operation])
        print(f"ID: {operations[operation]['id']}")
        print(f"Сумма в рублях: {rub:.2f} RUB")
        print(f"Сумма в долларах: {usd:.2f} USD")
        print(f"Сумма в евро: {eur:.2f} EUR")
        print("---")
        logger.info("Вывод суммы транзакции в валютах отработал")
    else:
        break

    # Пример использования функций
if __name__ == "__main__":
    logger.info("Запуск примера использования функций utils")
    transactions = read_transactions_from_json()
    for transaction in transactions[:5]:  # Обрабатываем первые 5 транзакций
        rub, usd, eur = transaction_amount(transaction)
        logger.info(f"ID: {transaction['id']}, RUB: {rub:.2f}, USD: {usd:.2f}, EUR: {eur:.2f}")

