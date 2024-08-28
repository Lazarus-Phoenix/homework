from masks import get_mask_account, get_mask_card_number # импорт модуля проекта
from datetime import datetime #импорт библиотеки обработки времени Python

def mask_account_card(check: str) -> str:
    """
    Принимает на вход номер счёта и данные карты, и маскирует их при возврате
    """
    if "Счет" in check:

        return f"Счёт {get_mask_account(check)}"

    letters = ""
    numbers = ""

    # Перебор каждого символа в исходной строке
    for char in check:
        if char.isdigit():  # Проверка, является ли символ цифрой
            numbers += char  # Добавление к числовым значениям
        else:
            letters += char  # Добавление к буквенным значениям

    # Вывод результатов
    return f"{letters.strip()} {get_mask_card_number(numbers)}"  # Используем strip() для удаления пробелов по краям


print(mask_account_card("Maestro 1596837868705199"))
print(mask_account_card("Счет 64686473678894779589"))
print(mask_account_card("MasterCard 7158300734726758"))
print(mask_account_card("Счет 35383033474447895560"))
print(mask_account_card("Visa Classic 6831982476737658"))
print(mask_account_card("Visa Platinum 8990922113665229"))
print(mask_account_card("Visa Gold 5999414228426353"))
print(mask_account_card("Счет 73654108430135874305"))


def get_date(date_string):
    """
    Функция конвертер формата отображения даты
    """
    # Преобразование строки в объект datetime
    dt = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%f")

    # Форматирование объекта datetime в строку с желаемым форматом
    formatted_date = dt.strftime("%d.%m.%Y")

    return formatted_date


# Пример использования функции
date_string = "2024-03-11T02:26:18.671407"
formatted_date = get_date(date_string)
print(formatted_date)  # Вывод: "11.03.2024"
