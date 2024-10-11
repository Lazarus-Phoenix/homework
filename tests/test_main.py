import pytest
import os
from src.processing import filter_by_state, sort_by_date, filter_by_description, count_operations_by_category
from src.utils import read_transactions_from_json
from src.csv_reader import read_csv
from src.xlsx_reader import read_xlsx

# Функция для получения пути к файлам в директории data
def get_data_file_path(filename):
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(project_root, "data")
    return os.path.join(data_dir, filename)

# Тестовые данные из JSON-файла
@pytest.fixture
def json_operations():
    return read_transactions_from_json(get_data_file_path("operations.json"))

# Тестовые данные из CSV-файла
@pytest.fixture
def csv_operations():
    return read_csv(get_data_file_path("operations.csv"))

# Тестовые данные из XLSX-файла
@pytest.fixture
def xlsx_operations():
    return read_xlsx(get_data_file_path("operations.xlsx"))

def test_filter_by_state(json_operations):
    filtered_operations = filter_by_state(json_operations, "EXECUTED")
    assert len(filtered_operations) > 0
    assert all(op["state"] == "EXECUTED" for op in filtered_operations)


def test_filter_by_description(json_operations):
    filtered_operations = filter_by_description(json_operations, "Перевод")
    assert len(filtered_operations) > 0
    assert all("Перевод" in op["description"] for op in filtered_operations)

def test_count_operations_by_category(json_operations):
    category_counts = count_operations_by_category(json_operations)
    assert len(category_counts) > 0
    assert all(count > 0 for count in category_counts.values())

@pytest.mark.parametrize("file_reader", ["json_operations", "csv_operations", "xlsx_operations"])
def test_file_reading(file_reader, request):
    operations = request.getfixturevalue(file_reader)
    assert len(operations) > 0
    assert all(isinstance(op, dict) for op in operations)
