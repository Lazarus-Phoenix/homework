import logging
import os
from datetime import datetime

# Получаем путь к корневой директории проекта
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Создаем директорию для логов в корне проекта, если она не существует
log_dir = os.path.join(project_root, "logs")
os.makedirs(log_dir, exist_ok=True)

# Получаем логгер для модуля utils
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Создаем файловый обработчик с режимом 'w' для перезаписи
file_handler = logging.FileHandler(os.path.join(log_dir, "log_masks.log"), mode="w")
file_handler.setLevel(logging.DEBUG)

# Создаем консольный обработчик для проверки на серьёзные проблемы в работе кода.
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Создаем форматтер
formatter = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s")

# Добавляем форматтер к обработчикам
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Добавляем обработчики к логгеру
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Записываем время запуска программы
start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"Программа запущена в {start_time}")

logger.debug("Debug message")


def get_mask_card_number(string_number: str) -> str:
    """принимает на вход номер карты в виде числа и возвращает
    маску номера по правилу XXXX XX** **** XXXX"""
    logger.debug(f"Вызван get_mask_card_number с аргументом: {string_number}")
    number_card = str(string_number)
    if number_card == "":
        logger.warning("Получена пустая строка для маскирования карты")
        return "Введите корректный номер"

    return f"{number_card[0:4]} {number_card[4:6]}** **** {number_card[12:16]}"


def get_mask_account(account_list: str) -> str:
    """принимает на вход номер счета в виде числа и возвращает
    маску номера по правилу **XXXX"""
    logger.debug(f"Вызван get_mask_account с аргументом: {account_list}")
    account_string = str(account_list)
    if account_string == "":
        logger.warning("Получена пустая строка для маскирования счета")
        return "Введите корректный номер"

    return f"** {account_string[-4:]}"


# Пример использования функций
if __name__ == "__main__":
    logger.info("Запуск примера использования функций маскирования")
    card = get_mask_card_number("7000792289606361")
    account = get_mask_account("73654108430135874305")
    print(f"Маска карты: {card}")
    print(f"Маска счета: {account}")
    logger.info(f"Маска карты: {card}")
    logger.info(f"Маска счета: {account}")
