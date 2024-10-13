import pytest
import os
import pandas as pd
from src.xlsx_reader import read_xlsx

@pytest.fixture
def sample_xlsx_file(tmp_path):
    xlsx_file = tmp_path / "test_operations.xlsx"
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
    df.to_excel(xlsx_file, index=False)
    return xlsx_file

# Тест чтения XLSX-файла
def test_read_xlsx(sample_xlsx_file):
    # Читаем XLSX-файл
    operations = read_xlsx(str(sample_xlsx_file))
    
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
    assert float(first_op["operationAmount"]["amount"]) == 100.0  # Преобразуем в float перед сравнением
    assert first_op["operationAmount"]["currency"]["code"] == "RUB"
    assert first_op["description"] == "Перевод организации"
    assert first_op["from"] == "Счет 1234567890123456"
    assert first_op["to"] == "Счет 9876543210987654"
    
    # Добавляем дополнительную проверку для отладки
    print(f"Type of id: {type(first_op['id'])}")
    print(f"Value of id: {first_op['id']}")
    print(f"Type of amount: {type(first_op['operationAmount']['amount'])}")
    print(f"Value of amount: {first_op['operationAmount']['amount']}")

def test_read_xlsx_empty_file(tmp_path):
    empty_file = tmp_path / "empty_file.xlsx"
    empty_file.touch()
    
    operations = read_xlsx(str(empty_file))
    assert operations == []

def test_read_xlsx_invalid_format(tmp_path):
    invalid_file = tmp_path / "invalid_file.txt"
    invalid_file.write_text("Это не XLSX-файл")
    
    operations = read_xlsx(str(invalid_file))
    assert operations is None or operations == []

