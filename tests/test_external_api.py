import unittest
from unittest.mock import patch
import requests

from src.external_api import get_exchange_rate


class TestGetExchangeRate(unittest.TestCase):
    """
    Тестовый класс для проверки функции get_exchange_rate из модуля external_api.
    """

    def test_valid_base_currency(self):
        """
        Проверка корректной работы функции при валидной базовой валюте.

        Ожидаемый результат: функция должна вернуть значение 1.0 для USD.
        """
        with patch('requests.get') as mock_get:
            mock_response = {
                "rates": {"RUB": 1.0}
            }
            mock_get.return_value.json.return_value = mock_response
            mock_get.return_value.status_code = 200

            result = get_exchange_rate("USD")

            self.assertEqual(result, 1.0)

    def test_invalid_base_currency(self):
        """
        Проверка обработки неверных базовых валют.

        Ожидаемый результат: вызывается исключение ValueError для EUR.
        """
        with patch('requests.get') as mock_get:
            mock_response = {}
            mock_get.return_value.json.return_value = mock_response
            mock_get.return_value.status_code = 200

            with self.assertRaises(ValueError):
                get_exchange_rate("EUR")

    def test_api_request_failure(self):
        """
        Проверка обработки ошибок при запросе к API.

        Ожидаемый результат: вызывается исключение ValueError при возникновении ошибки запроса.
        """
        with patch('requests.get') as mock_get:
            mock_get.side_effect = requests.exceptions.RequestException("Test error")

            with self.assertRaises(ValueError):
                get_exchange_rate("USD")

    def test_no_rub_rate_in_response(self):
        """
        Проверка обработки случая, когда RUB не присутствует в ответе от API.

        Ожидаемый результат: вызывается исключение ValueError.
        """
        with patch('requests.get') as mock_get:
            mock_response = {
                "rates": {"GBP": 1.5}
            }
            mock_get.return_value.json.return_value = mock_response
            mock_get.return_value.status_code = 200

            with self.assertRaises(ValueError):
                get_exchange_rate("GBP")


if __name__ == '__main__':
    unittest.main()
