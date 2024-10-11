import pytest
import os
import pandas as pd
from src.csv_reader import read_csv


# Создаем фикстуру для тестового CSV-файла
@pytest.fixture
def sample_csv_file(tmp_path):
    # Создаем временный CSV-файл
    csv_file = tmp_path / "test_operations.csv"
    data = {
        "id": [1, 2, 3],
        "state": ["EXECUTED", "CANCELED", "EXECUTED"],
        "date": ["2023-01-01T00:00:00.000000", "2023-01-02T00:00:00.000000", "2023-01-03T00:00:00.000000"],
        "amount": [100.0, -50.0, 200.0],
        "currency_code": ["RUB", "USD", "EUR"],
        "description": ["Перевод организации", "Перевод со счета на счет", "Перевод с карты на карту"],
        "from": ["Счет 1234567890123456", "Счет 9876543210987654", "Visa Classic 1234567890123456"],
        "to": ["Счет 9876543210987654", "Счет 1234567890123456", "Visa Platinum 9876543210987654"]
    }
    df = pd.DataFrame(data)
    df.to_csv(csv_file, index=False, sep=';')
    return csv_file


# Тест чтения CSV-файла
def test_read_csv(sample_csv_file):
    # Читаем CSV-файл
    operations = read_csv(str(sample_csv_file))
    
    # Проверяем, что функция вернула список словарей
    assert isinstance(operations, list)
    assert all(isinstance(op, dict) for op in operations)
    
    # Проверяем количество операций
    assert len(operations) == 3
    
    # Проверяем структуру первой операции
    first_op = operations[0]
    assert str(first_op["id"]) == "1"  # Преобразуем в строку перед сравнением
    assert first_op["state"] == "EXECUTED"
    assert first_op["date"] == "2023-01-01T00:00:00.000000"
    assert str(first_op["operationAmount"]["amount"]) == "100.0"  # Преобразуем в строку перед сравнением
    assert first_op["operationAmount"]["currency"]["code"] == "RUB"
    assert first_op["description"] == "Перевод организации"
    assert first_op["from"] == "Счет 1234567890123456"
    assert first_op["to"] == "Счет 9876543210987654"
    
    # Добавляем дополнительную проверку для отладки
    print(f"Type of id: {type(first_op['id'])}")
    print(f"Value of id: {first_op['id']}")
    print(f"Type of amount: {type(first_op['operationAmount']['amount'])}")
    print(f"Value of amount: {first_op['operationAmount']['amount']}")
    
# Тест с пустым файлом
def test_read_csv_empty_file(tmp_path):
    empty_file = tmp_path / "empty_file.csv"
    empty_file.touch()
    
    operations = read_csv(str(empty_file))
    assert operations == []

# Тест с некорректным форматом файла
def test_read_csv_invalid_format(tmp_path):
    invalid_file = tmp_path / "invalid_file.txt"
    invalid_file.write_text("Это не CSV-файл")
    
    # Проверяем, что функция вернула пустой список или None
    operations = read_csv(str(invalid_file))
    assert operations is None or operations == []