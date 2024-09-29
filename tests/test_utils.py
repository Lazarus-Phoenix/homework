import unittest
from unittest.mock import patch
from src.utils import read_transactions_from_json


class TestReadTransactionsFromJson(unittest.TestCase):
    """
    Тестовый класс для проверки функции read_transactions_from_json из модуля utils.

    Этот класс содержит несколько методов-тестов, которые проверяют различные сценарии работы функции:
    - Проверка существования файла
    - Проверка отсутствия файла
    - Проверка неверного расширения файла
    - Проверка валидных данных JSON
    - Проверка некорректных данных JSON

    Каждый метод использует патчи (mocks) для имитации различных условий и проверяет результат выполнения функции.
    """

    def test_file_exists(self):
        """
        Проверка, что функция корректно обрабатывает случай, когда файл существует.

        Используется патч для os.path.exists и json.load для имитации валидных данных.
        """
        with patch('os.path.exists', return_value=True), \
                patch('json.load', return_value=[{'date': '2023-01-01', 'amount': 100}]):
            result = read_transactions_from_json()
            self.assertEqual(result, [{'date': '2023-01-01', 'amount': 100}])

    def test_file_not_exists(self):
        """
        Проверка, что функция корректно обрабатывает случай, когда файл не существует.

        Используется патч для os.path.exists, чтобы вернуть False.
        """
        with patch('os.path.exists', return_value=False):
            result = read_transactions_from_json()
            self.assertEqual(result, [])

    def test_invalid_file_extension(self):
        """
        Проверка, что функция корректно обрабатывает случай с неверным расширением файла.

        Используется патч для os.path.join, чтобы вернуть путь с неверным расширением.
        """
        with patch('os.path.exists', return_value=True), \
                patch('os.path.join', return_value='/invalid/path'):
            result = read_transactions_from_json()
            self.assertEqual(result, [])

    def test_valid_json_data(self):
        """
        Проверка, что функция корректно обрабатывает валидные данные JSON.

        Используются патчи для os.path.exists и json.load для имитации валидных данных.
        """
        with patch('os.path.exists', return_value=True), \
                patch('os.path.join', return_value='/valid/path'), \
                patch('json.load', return_value=[{'date': '2023-01-01', 'amount': 100}]):
            result = read_transactions_from_json()
            self.assertEqual(result, [])

    def test_invalid_json_data(self):
        """
        Проверка, что функция корректно обрабатывает некорректные данные JSON.

        Используется патч для json.load с вызовом ValueError.
        """
        with patch('os.path.exists', return_value=True), \
                patch('os.path.join', return_value='/valid/path'), \
                patch('json.load', side_effect=ValueError("Invalid JSON")):
            result = read_transactions_from_json()
            self.assertEqual(result, [])
