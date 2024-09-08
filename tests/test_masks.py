import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize(
    "number_card, mask",
    [
        ("1234567890123456", "1234 56** **** 3456"),
        ("9876543210123456", "9876 54** **** 3456"),
        ("", "Введите корректный номер"),
    ],
)
def test_get_mask_card_number(number_card, mask):
    assert get_mask_card_number(number_card) == mask


@pytest.mark.parametrize(
    "account_string, mask", [("12345678901234567890", "** 7890"), ("98765432109876543210", "** 3210")]
)
def test_get_mask_account(account_string, mask):
    assert get_mask_account(account_string) == mask
