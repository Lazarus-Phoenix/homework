# Импорт необходимых модулей
from src.external_api import get_exchange_rate
from typing import Dict


# Функция для конвертации транзакции в рубли
def convert_transaction_to_rubles(transaction: Dict[str, str]) -> float:
    """
    Конвертирует сумму транзакции из указанной валюты в рубли.

    Args:
        transaction (Dict[str, str]): Словарь с информацией о транзакции.
            Должен содержать ключи 'amount' и 'currency'.

    Returns:
        float: Сумма транзакции в рублях, округленная до двух знаков после запятой.

    Raises:
        ValueError: Если указанная валюта не поддерживается.
    """

    # Извлечение суммы из словаря транзакции и преобразование в число с плавающей точкой
    amount = float(transaction['amount'])

    # Получение кода валюты из словаря транзакции и приведение к верхнему регистру
    currency = transaction['currency'].upper()

    # Проверка валюты и выполнение соответствующей конвертации
    if currency == 'USD' or currency == 'EUR':
        # Получение курса обмена для указанной валюты
        exchange_rate = get_exchange_rate(currency)

        # Конвертация суммы в рубли
        amount_in_rubles = amount * exchange_rate
    elif currency == 'RUB':
        # Если валюта уже рубли, то конвертация не требуется
        amount_in_rubles = amount
    else:
        # Если валюта не поддерживается, вызывается исключение
        raise ValueError(f"Unsupported currency: {currency}")

    # Округление результата до двух знаков после запятой и возврат
    return round(amount_in_rubles, 2)


# Пример использования функции
if __name__ == "__main__":
    # Создание примерной транзакции
    transaction = {
        'amount': '1',
        'currency': 'USD'
    }

    # Выполнение конвертации и вывод результата
    result = convert_transaction_to_rubles(transaction)
    print(f"{transaction['amount']} {transaction['currency']} = {result} RUB")
