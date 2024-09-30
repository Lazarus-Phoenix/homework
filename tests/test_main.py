import unittest
from src.main import convert_transaction_to_rubles


class TestConvertTransactionToRubles(unittest.TestCase):

    def test_usd_conversion(self):
        # Подготовка данных
        transaction = {'amount': '100', 'currency': 'USD'}

        # Выполнение функции
        result = convert_transaction_to_rubles(transaction)

        # Проверка результата
        self.assertAlmostEqual(result, 9294.00, places=2)

    def test_eur_conversion(self):
        # Подготовка данных
        transaction = {'amount': '50', 'currency': 'EUR'}

        # Выполнение функции
        result = convert_transaction_to_rubles(transaction)

        # Проверка результата
        self.assertAlmostEqual(result, 5190.50, places=2)

    def test_rub_conversion(self):
        # Подготовка данных
        transaction = {'amount': '2000', 'currency': 'RUB'}

        # Выполнение функции
        result = convert_transaction_to_rubles(transaction)

        # Проверка результата
        self.assertAlmostEqual(result, 2000.00, places=2)

    def test_invalid_currency(self):
        # Подготовка данных
        transaction = {'amount': '500', 'currency': 'GBP'}

        # Проверка возникновения исключения
        with self.assertRaises(ValueError) as cm:
            convert_transaction_to_rubles(transaction)

        # Проверка сообщения об ошибке
        self.assertEqual(str(cm.exception), "Unsupported currency: GBP")

    def test_invalid_amount(self):
        # Подготовка данных
        transaction = {'amount': 'abc', 'currency': 'USD'}

        # Проверка возникновения исключения
        with self.assertRaises(ValueError) as cm:
            convert_transaction_to_rubles(transaction)

        # Проверка сообщения об ошибке
        self.assertEqual(str(cm.exception), "could not convert string to float: 'abc'")

if __name__ == '__main__':
    unittest.main()
