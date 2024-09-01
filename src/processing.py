from datetime import datetime
from typing import Any, Dict, List


def filter_by_state(operations: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """Фильтрация операций по состоянию"""
    filtered_operations = [i for i in operations if i["state"] == state]
    return filtered_operations


def sort_by_date(filtered_operations: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
    """Сортировка операций по дате"""
    sorted_list = sorted(
        filtered_operations, key=lambda x: datetime.strptime(x["date"], "%Y-%m-%dT%H:%M:%S.%f"), reverse=reverse
    )
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
