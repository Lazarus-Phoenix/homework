from datetime import datetime

import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "check, mask",
    [
        ("Visa Platinum 1234567890123456", "Visa Platinum 1234 56** **** 3456"),
        ("Maestro 9876543210123456", "Maestro 9876 54** **** 3456"),
        ("Счет 1234567890123456790", "Некорректный номер счёта"),
        ("Счет 12345678901234567890", "Счет ** 7890"),
    ],
)
def test_mask_account_card(check, mask):
    assert mask_account_card(check) == mask


@pytest.mark.parametrize(
    "date_string, expected",
    [
        ("2024-04-15T14:30:45.123456", "15.04.2024"),
        ("2025-01-20T23:59:59.999999", "20.01.2025"),
        ("2023-06-25T12:00:00.000001", "25.06.2023"),
        ("2026-10-31T07:45:32.987654", "31.10.2026"),
        ("2027-02-28T19:21:43.567890", "28.02.2027"),
    ],
)
def test_get_date(date_string, expected):
    assert get_date(date_string) == expected


def test_sorting_by_dates():
    # Список словарей с датами
    items = [
        {"date": "2024-04-15T14:30:45.123456"},
        {"date": "2025-01-20T23:59:59.999999"},
        {"date": "2023-06-25T12:00:00.000001"},
        {"date": "2026-10-31T07:45:32.987654"},
        {"date": "2027-02-28T19:21:43.567890"},
    ]

    # Сортировка по убыванию
    sorted_descending = sorted(items, key=lambda x: datetime.strptime(get_date(x["date"]), "%d.%m.%Y"), reverse=True)

    assert [item["date"] for item in sorted_descending] == [
        "2027-02-28T19:21:43.567890",
        "2026-10-31T07:45:32.987654",
        "2025-01-20T23:59:59.999999",
        "2024-04-15T14:30:45.123456",
        "2023-06-25T12:00:00.000001",
    ]

    # Сортировка по возрастанию
    sorted_ascending = sorted(items, key=lambda x: datetime.strptime(get_date(x["date"]), "%d.%m.%Y"))

    assert [item["date"] for item in sorted_ascending] == [
        "2023-06-25T12:00:00.000001",
        "2024-04-15T14:30:45.123456",
        "2025-01-20T23:59:59.999999",
        "2026-10-31T07:45:32.987654",
        "2027-02-28T19:21:43.567890",
    ]


@pytest.mark.parametrize(
    "invalid_date_string",
    [
        "2024-04-15T14:30:45",  # Отсутствуют микросекунды
        "2024-04-15T14:30:45.123456789",  # Слишком много цифр после запятой
        "2024-04-15T24:30:45.123456",  # Неправильное время
        "2024-13-15T14:30:45.123456",  # Неправильный месяц
        "2024-04-32T14:30:45.123456",  # Неправильный день
        "2024-04-15T14:30:45.123456Z",  # Неправильный формат
        "invalid-date-string",  # Полностью некорректная строка
    ],
)
def test_invalid_date_formats(invalid_date_string):
    assert get_date(invalid_date_string) == ""
