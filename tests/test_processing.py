from datetime import datetime
import pytest
from typing import List, Dict, Any

from src.processing import filter_by_state, sort_by_date  # Импорт тестируемых функций

# Фикстура для генерации тестовых данных
@pytest.fixture(scope="function")
def sample_data() -> List[Dict[str, Any]]:
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-01-01T00:00:00.000000"},
        {"id": 2, "state": "EXECUTED", "date": "2023-01-03T00:00:00.000000"},
        {"id": 3, "state": "CANCELED", "date": "2023-01-04T00:00:00.000000"},
        {"id": 4, "state": "EXECUTED", "date": "2023-01-05T00:00:00.000000"},
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
    # Фильтрация операций по заданному состоянию
    filtered = filter_by_state(sample_data, state)

    # Проверка количества отфильтрованных элементов
    assert len(filtered) == expected_count

    # Проверка состояния каждого отфильтрованного элемента
    for item in filtered:
        assert item["state"] == state

# Тест сортировки по убыванию (по умолчанию)
def test_sort_by_date_descending(sample_data: List[Dict[str, Any]]):
    # Фильтрация и сортировка операций
    sorted_data = sort_by_date(filter_by_state(sample_data))

    # Преобразование дат в объекты datetime для сравнения
    dates = [datetime.strptime(item["date"].split('.')[0], "%Y-%m-%dT%H:%M:%S") for item in sorted_data]

    # Проверка правильности сортировки
    assert dates == sorted(dates, reverse=True)

# Тест сортировки по возрастанию
def test_sort_by_date_ascending(sample_data: List[Dict[str, Any]]):
    # Фильтрация и сортировка операций в порядке возрастания
    sorted_data = sort_by_date(filter_by_state(sample_data), reverse=False)

    dates = [datetime.strptime(item["date"].split('.')[0], "%Y-%m-%dT%H:%M:%S") for item in sorted_data]

    # Проверка правильности сортировки
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
