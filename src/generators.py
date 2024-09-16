
transactions = (
    [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702"
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188"
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160"
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {
                "amount": "56883.54",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229"
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {
                "amount": "67314.70",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657"
        }
    ]
)


def filter_by_currency(transaction_list: list, code: str) -> iter:
    """
    Функция создает итератор, который фильтрует транзакции по заданному значению валюты.
    Если список транзакций пуст, возвращает сообщение "Нет транзакций.".
    Иначе перебирается по списку, проверяется код валюты каждой транзакции и возвращается
    соответствующая транзакция или None для неподходящих транзакций.
    """

    # Проверяем, пуст ли список транзакций
    if not transaction_list:
        yield "Нет транзакций."

    else:
        # Итерируемся по списку транзакций
        for transaction_pay in transaction_list:
            # Получаем код валюты из транзакции
            currency_code = transaction_pay.get("operationAmount", {}).get("currency", {}).get("code")

            # Если код валюты совпадает с заданным значением, возвращаем транзакцию
            if currency_code == code:
                yield transaction_pay
            else:
                yield None


pay_transaction = filter_by_currency(transactions,"USD")
for _ in range(3):
    result = next(pay_transaction)
    if result:
        print(result)
    else:
        print("Транзакции в данной валюте отсутствуют")


def transaction_descriptions(transaction_list: list, descriptions: str) -> iter:
    """ Функция создает итератор, который возвращает описания операций из переданного списка транзакций.
    Если список пуст, возвращает сообщение "Нет транзакций.". Иначе итерируется по списку и возвращает
    описание каждой транзакции.
    """

    if not transaction_list:
        yield "Нет описания."


    else:

        for pay in transaction_list:
            yield pay.get("description")


pay_description = transaction_descriptions(transactions,"descriptions")
for _ in range(5):
    print(next(pay_description))


def card_number_generator(start, stop):
    """ Функция-генератор, которая создает итератор для генерации номеров банковских карт.
    Принимает начальный и конечный значения диапазона. Генерирует номера карт от start до stop,
     добавляя необходимое количество нулей слева для достижения общей длины 16 символов.
    """
    for i in range(start, stop + 1):
        num_str = str(i)
        padding = '0' * (16 - len(num_str))
        yield padding + num_str
for card_number in card_number_generator(1, 5):
    print(card_number)

