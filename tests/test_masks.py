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
    "account_string, mask",
    [
        ("12345678901234567890", "** 7890"),
        ("98765432109876543210", "** 3210"),
        ("11122233344455566670", "** 6670"),
        ("88877766655544433320", "** 3320"),
        ("99988877766655544430", "** 4430"),
        ("00011122233344455560", "** 5560"),
        ("77766655544433322080", "** 2080"),
        ("66655544433322299090", "** 9090"),
        ("55544433322211100000", "** 0000"),
        ("44433322211100001110", "** 1110"),
        ("", "Введите корректный номер")

    ]
)
def test_get_mask_account(account_string, mask):
    assert get_mask_account(account_string) == mask
