# Импорт необходимых библиотек
import os
import requests


def get_exchange_rate(base_currency: str) -> float:
    """
    Получает курс обмена валюты из API exchangerate-api.com.

    Args:
        base_currency (str): Код валюты для получения курса обмена в рубли.

    Returns:
        float: Курс обмена указанной валюты в рубли.

    Raises:
        ValueError: Если не удалось получить курс обмена или если API запрос завершился ошибкой.
        При возникновении проблем при выполнении HTTP-запроса.
    """

    try:
        # Получаем ключ API из переменной окружения
        api_key = os.getenv('EXCHANGE_RATE_API_KEY')

        # Формируем URL запроса к API
        url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"

        # Выполняем GET-запрос к API
        response = requests.get(url)
        response.raise_for_status()  # Возвратит исключение в случае ошибки ответа

        #  JSON-ответ
        data = response.json()

        # Проверяем наличие необходимых данных в ответе
        if 'rates' not in data or 'RUB' not in data['rates']:
            raise ValueError(f"No exchange rate found for {base_currency} to RUB")

        # Получаем курс обмена в рубли
        rub_rate = data['rates']['RUB']

        # Проверяем, что курс обмена не None и приводим его к типу float
        if rub_rate is None:
            raise ValueError(f"No exchange rate found for {base_currency} to RUB")

        # Возвращаем курс обмена как число с плавающей точкой
        return float(rub_rate)

    except requests.RequestException as e:
        # Обрабатываем возможные проблемы с HTTP-запросом
        raise ValueError(f"API request failed: {str(e)}")
