from datetime import datetime
import pytest
from typing import List, Dict, Any
from src.processing import filter_by_state, sort_by_date, filter_by_description, count_operations_by_category

# Фикстура для генерации тестовых данных
@pytest.fixture(scope="function")
def sample_data() -> List[Dict[str, Any]]:
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-01-01T00:00:00.000000", "description": "Перевод организации"},
        {"id": 2, "state": "EXECUTED", "date": "2023-01-03T00:00:00.000000", "description": "Перевод со счета на счет"},
        {"id": 3, "state": "CANCELED", "date": "2023-01-04T00:00:00.000000", "description": "Перевод с карты на карту"},
        {"id": 4, "state": "EXECUTED", "date": "2023-01-05T00:00:00.000000", "description": "Перевод организации"},
    ]

# Параметризованный тест для функции filter_by_state
@pytest.mark.parametrize(
    "state, expected_count",
    [
        ("EXECUTED", 3),
        ("CANCELED", 1),
    ],
)
def test_filter_by_state(sample_data: List[Dict[str, Any]], state: str, expected_count: int):
    filtered = filter_by_state(sample_data, state)
    assert len(filtered) == expected_count
    for item in filtered:
        assert item["state"] == state

# Тест сортировки по убыванию (по умолчанию)
def test_sort_by_date_descending(sample_data: List[Dict[str, Any]]):
    # Фильтрация и сортировка операций
    sorted_data = sort_by_date(filter_by_state(sample_data))
    # Преобразование дат в объекты datetime для сравнения
    dates = [datetime.strptime(item["date"].split('.')[0], "%Y-%m-%dT%H:%M:%S") for item in sorted_data]
    assert dates == sorted(dates, reverse=True)

# Тест сортировки по возрастанию
def test_sort_by_date_ascending(sample_data: List[Dict[str, Any]]):
    sorted_data = sort_by_date(filter_by_state(sample_data), reverse=False)
    dates = [datetime.strptime(item["date"].split('.')[0], "%Y-%m-%dT%H:%M:%S") for item in sorted_data]
    assert dates == sorted(dates)

# Тест с пустым списком
def test_sort_by_date_empty_list():
    empty_list: List[Dict[str, Any]] = []
    sorted_result = sort_by_date(empty_list)
    assert sorted_result == []

# Тест с одним элементом
def test_sort_by_date_single_item():
    single_item_list: List[Dict[str, Any]] = [{"id": 1, "state": "EXECUTED", "date": "2023-01-01T00:00:00.000000"}]
    sorted_result = sort_by_date(single_item_list)
    assert sorted_result == single_item_list

def test_filter_by_description(sample_data: List[Dict[str, Any]]):
    filtered_data = filter_by_description(sample_data, "Перевод")
    assert len(filtered_data) == 4
    for item in filtered_data:
        assert "Перевод" in item["description"]

def test_count_operations_by_category(sample_data: List[Dict[str, Any]]):
    category_counts = count_operations_by_category(sample_data)
    assert category_counts == {"EXECUTED": 3, "CANCELED": 1}

def test_count_operations_by_category_empty_list():
    empty_list: List[Dict[str, Any]] = []
    category_counts = count_operations_by_category(empty_list)
    assert category_counts == {}

def test_count_operations_by_category_single_item():
    single_item_list: List[Dict[str, Any]] = [{"id": 1, "state": "EXECUTED", "date": "2023-01-01T00:00:00.000000"}]
    category_counts = count_operations_by_category(single_item_list)
    assert category_counts == {"EXECUTED": 1}
