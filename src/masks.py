def get_mask_card_number(string_number: str) -> str:
    """принимает на вход номер карты в виде числа и возвращает
    маску номера по правилу XXXX XX** **** XXXX"""
    number_card = str(string_number)

    return f"{number_card[0:4]} {number_card[4:6]}** **** {number_card[12:16]}"


def get_mask_account(account_list: str) -> str:
    """принимает на вход номер счета в виде числа и возвращает
    маску номера по правилу **XXXX"""
    accaunt_string = str(account_list)

    return f"** {accaunt_string[16:20]}"


card = str(get_mask_card_number(7000792289606361))
accaunt = str(get_mask_account(73654108430135874305))

if __name__ == "__main__":
    print(card)
    print(accaunt)
