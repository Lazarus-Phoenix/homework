import re
from collections import Counter
from datetime import datetime
from typing import Any, Dict, List


def filter_by_description(operations: List[Dict[str, Any]], search_string: str) -> List[Dict[str, Any]]:
    """Фильтрация операций по описанию"""
    pattern = re.compile(search_string, re.IGNORECASE)
    filtered_operations = [op for op in operations if pattern.search(op.get("description", ""))]
    return filtered_operations


def count_operations_by_category(operations: List[Dict[str, Any]]) -> Dict[str, int]:
    """Подсчет количества операций по категориям"""
    categories = Counter()
    for op in operations:
        category = op.get("state", "").strip().upper()
        categories[category] += 1
    return categories


def filter_by_state(operations: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """Фильтрация операций по состоянию"""
    filtered_operations = [i for i in operations if i.get("state") == state]
    return filtered_operations


def sort_by_date(filtered_operations: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
    """Сортировка операций по дате"""

    def parse_date(date_string):
        if not date_string:
            return datetime.min
        for fmt in ["%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d %H:%M:%S"]:
            try:
                return datetime.strptime(date_string, fmt)
            except ValueError:
                pass
            return datetime.min

    sorted_list = sorted(filtered_operations, key=lambda x: parse_date(x.get("date", "")), reverse=reverse)
    return sorted_list


# Пример использования
data = [
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
]

filtered_data = filter_by_state(data)
sorted_data = sort_by_date(filtered_data)

print(sorted_data)
