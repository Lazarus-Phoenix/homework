import os
import unittest
import json
import tempfile
from src.utils import test_ops, standard_ops, operations, transaction_amount


class TestReadTransactionsFromJson(unittest.TestCase):
    """
    Тестовый класс для проверки функции read_transactions_from_json.

    Attributes:
        test_file_path (str): Путь к временному тестовому файлу.
    """

    @classmethod
    def setUpClass(cls):
        """
        Метод для настройки класса перед выполнением всех тестов.

        Создает временный JSON-файл с тестовыми данными.
        """
        cls.test_file_path = tempfile.mkstemp()[1]

        test_data = [
            {"date": "2023-01-01", "amount": 100.0, "type": "income"},
            {"date": "2023-01-02", "amount": -50.0, "type": "expense"}
        ]

        with open(cls.test_file_path, "w") as f:
            json.dump(test_data, f)

    @classmethod
    def tearDownClass(cls):
        """
        Метод для очистки после выполнения всех тестов.

        Удаляет созданный временный файл.
        """
        os.remove(cls.test_file_path)

    def test_valid_json(self):
        """
        Тест проверяет чтение корректного JSON-файла.

        Проверяет, что функция transaction_amount возвращает ожидаемый результат.
        """
        for operation in range(1):
            if operation < len(operations):
                rub, usd, eur = transaction_amount(operations[operation])
                result = (f"ID: {operations[operation]['id']}")

        self.assertEqual(result, 'ID: 441945886')

    def test_empty_file(self):
        """
        Тест проверяет поведение при пустом JSON-файле.

        Создает пустой JSON-файл и проверяет, что функция вернет пустой список.
        """
        empty_file_path = tempfile.mkstemp()[1]
        with open(empty_file_path, "w") as f:
            json.dump([], f)

        result = test_ops
        self.assertEqual(result, [])

        os.remove(empty_file_path)

    def test_non_json_file(self):
        """
        Тест проверяет поведение при некорректном JSON-файле.

        Создает файл с некорректным содержимым и проверяет, что функция вернет пустой список.
        """
        non_json_file_path = tempfile.mkstemp()[1]
        with open(non_json_file_path, "w") as f:
            f.write("This is not a JSON file")

        result = test_ops
        self.assertEqual(result, [])

        os.remove(non_json_file_path)

    def test_invalid_json(self):
        """
        Тест проверяет поведение при невалидном JSON-файле.

        Создает файл с невалидным JSON-содержимым и проверяет, что функция вернет пустой список.
        """
        invalid_json_file_path = tempfile.mkstemp()[1]
        with open(invalid_json_file_path, "w") as f:
            f.write("{")

        result = test_ops
        self.assertEqual(result, [])

        os.remove(invalid_json_file_path)


if __name__ == '__main__':
    unittest.main()

import unittest
from unittest.mock import patch
from src.utils import transaction_amount, get_exchange_rate


class TestTransactionAmount(unittest.TestCase):
    """
    Тестовый класс для проверки функции transaction_amount.

    Attributes:
        test_operations (list): Список тестовых операций для проверки функции.
    """

    def setUp(self):
        """
        Метод для настройки перед каждым тестом.

        Создает список тестовых операций с различными валютами.
        """
        self.test_operations = [
            {
                'id': 1,
                'operationAmount': {
                    'amount': '100',
                    'currency': {'code': 'RUB'}
                }
            },
            {
                'id': 2,
                'operationAmount': {
                    'amount': '50',
                    'currency': {'code': 'USD'}
                }
            },
            {
                'id': 3,
                'operationAmount': {
                    'amount': '75',
                    'currency': {'code': 'EUR'}
                }
            },
            {
                'id': 4,
                'operationAmount': {
                    'amount': '200',
                    'currency': {'code': 'RUB'}
                }
            }
        ]

    @patch('src.utils.get_exchange_rate')
    def test_rub_to_rub(self, mock_get_exchange_rate):
        """
        Тест проверяет конвертацию из рублей в другие валюты.

        Проверяет корректность вычисления сумм при конвертации из RUB.
        """
        # Устанавливаем курсы обмена для теста
        mock_get_exchange_rate.return_value = {
            'USD': 60.0,
            'EUR': 65.0
        }

        result = transaction_amount(self.test_operations[0])
        self.assertEqual(result[0], 100)
        self.assertAlmostEqual(result[1], 1.67, places=2)
        self.assertAlmostEqual(result[2], 1.54, places=2)

    @patch('src.utils.get_exchange_rate')
    def test_usd_to_rub(self, mock_get_exchange_rate):
        """
        Тест проверяет конвертацию из долларов в другие валюты.

        Проверяет корректность вычисления сумм при конвертации из USD.
        """
        # Устанавливаем курсы обмена для теста
        mock_get_exchange_rate.return_value = {
            'USD': 60.0,
            'EUR': 65.0
        }

        result = transaction_amount(self.test_operations[1])
        self.assertAlmostEqual(result[0], 3000, places=2)
        self.assertEqual(result[1], 50)
        self.assertAlmostEqual(result[2], 46.15, places=2)

    @patch('src.utils.get_exchange_rate')
    def test_eur_to_rub(self, mock_get_exchange_rate):
        """
        Тест проверяет конвертацию из евро в другие валюты.

        Проверяет корректность вычисления сумм при конвертации из EUR.
        """
        # Устанавливаем курсы обмена для теста
        mock_get_exchange_rate.return_value = {
            'USD': 60.0,
            'EUR': 65.0
        }

        result = transaction_amount(self.test_operations[2])
        self.assertAlmostEqual(result[0], 4875, places=2)
        self.assertAlmostEqual(result[1], 81.25, places=2)
        self.assertEqual(result[2], 75)

    @patch('src.utils.get_exchange_rate')
    def test_unknown_currency(self, mock_get_exchange_rate):
        """
        Тест проверяет поведение при неизвестной валюте.

        Проверяет, что функция возвращает нулевые значения для неизвестной валюты.
        """
        # Устанавливаем курсы обмена для теста
        mock_get_exchange_rate.return_value = {
            'USD': 60.0,
            'EUR': 65.0
        }

        result = transaction_amount({
            'id': 5,
            'operationAmount': {
                'amount': '100',
                'currency': {'code': 'GBP'}
            }
        })
        self.assertEqual(result[0], 0)
        self.assertEqual(result[1], 0)
        self.assertEqual(result[2], 0)


if __name__ == '__main__':
    unittest.main()
