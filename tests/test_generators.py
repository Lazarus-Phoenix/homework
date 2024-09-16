import pytest

from src.generators import transaction_descriptions, filter_by_currency, card_number_generator


def test_empty_list():
    """
    Тест функции с пустым списком транзакций.
    """
    empty_transactions = []  # Создаем пустой список для симуляции отсутствия транзакций
    filtered_transactions = filter_by_currency(empty_transactions, "RUB")  # Вызываем функцию

    # Проверяем, что функция вернула ожидаемое сообщение
    assert next(filtered_transactions) == "Нет транзакций."

    # Проверяем, что после сообщения генератор завершается
    with pytest.raises(StopIteration):
        next(filtered_transactions)


@pytest.fixture
def sample_transaction():
    """
    Фикстура для создания тестового списка транзакций.
    """
    return [
        {"operationAmount": {"currency": {"code": "RUB"}}},
        {"operationAmount": {"currency": {"code": "USD"}}},
        {"operationAmount": {"currency": {"code": "EUR"}}},
    ]


def test_filter_rub(sample_transaction):
    """
    Тест фильтрации транзакций по коду валюты RUB.
    """
    filtered_transactions = filter_by_currency(sample_transaction, "RUB")

    assert next(filtered_transactions) == sample_transaction[0]
    assert next(filtered_transactions) is None
    assert next(filtered_transactions) is None

    with pytest.raises(StopIteration):
        next(filtered_transactions)


def test_filter_usd(sample_transaction):
    """
    Тест фильтрации транзакций по коду валюты USD.
    """
    filtered_transactions = filter_by_currency(sample_transaction, "USD")

    assert next(filtered_transactions) is None
    assert next(filtered_transactions) == sample_transaction[1]
    assert next(filtered_transactions) is None

    with pytest.raises(StopIteration):
        next(filtered_transactions)


def test_filter_eur(sample_transaction):
    """
    Тест фильтрации транзакций по коду валюты EUR.
    """
    filtered_transactions = filter_by_currency(sample_transaction, "EUR")

    assert next(filtered_transactions) is None
    assert next(filtered_transactions) is None
    assert next(filtered_transactions) == sample_transaction[2]

    with pytest.raises(StopIteration):
        next(filtered_transactions)


def test_invalid_code(sample_transaction):
    """
    Тест фильтрации транзакций по несуществующему коду валюты.
    """
    filtered_transactions = filter_by_currency(sample_transaction, "GBP")

    # Проверяем, что все транзакции не соответствуют коду GBP и возвращаются None
    assert next(filtered_transactions) is None
    assert next(filtered_transactions) is None
    assert next(filtered_transactions) is None

    # Проверяем, что после всех транзакций генератор завершается
    with pytest.raises(StopIteration):
        next(filtered_transactions)


def test_empty_list():
    """
    Тест функции с пустым списком транзакций.
    """
    empty_transactions = []  # Создаем пустой список для симуляции отсутствия транзакций
    descriptions = transaction_descriptions(empty_transactions, "")  # Вызываем функцию

    # Проверяем, что функция вернула ожидаемое сообщение
    assert next(descriptions) == "Нет описания."

    # Проверяем, что после сообщения генератор завершается
    with pytest.raises(StopIteration):
        next(descriptions)


@pytest.fixture
def sample_transactions():
    """
    Фикстура для создания тестового списка транзакций.
    """
    return [
        {"description": "Перевод организации"},
        {"description": "Перевод со счета на счет"},
        {"description": "Перевод с карты на карту"},
    ]


def test_non_empty_list(sample_transactions):
    """
    Тест функции со списком транзакций.
    """
    descriptions = transaction_descriptions(sample_transactions, "")  # Вызываем функцию

    # Проверяем, что функция вернула описания всех транзакций в правильном порядке
    assert next(descriptions) == "Перевод организации"
    assert next(descriptions) == "Перевод со счета на счет"
    assert next(descriptions) == "Перевод с карты на карту"

    # Проверяем, что после всех транзакций генератор завершается
    with pytest.raises(StopIteration):
        next(descriptions)


def test_description_count(sample_transactions):
    """
    Тест, проверяющий количество возвращенных описаний.
    """
    descriptions = transaction_descriptions(sample_transactions, "")  # Вызываем функцию

    # Считаем количество возвращенных описаний
    description_count = sum(1 for _ in descriptions)

    # Проверяем, что количество описаний равно количеству транзакций
    assert description_count == len(sample_transactions)


def test_description_type(sample_transactions):
    """
    Тест, проверяющий тип возвращаемых значений.
    """
    descriptions = transaction_descriptions(sample_transactions, "")  # Вызываем функцию

    # Проверяем, что первое возвращенное значение является строкой
    assert isinstance(next(descriptions), str)


@pytest.fixture(
    params=[
        (1, 10),
        (100, 110),
        (99999, 99999),
    ]
)
def test_data(request):
    """
    Фикстура для создания набора тестовых данных для генератора номеров карт.

    Эта фикстура используется для параметризации тестов, позволяя проверить работу генератора
    с различными диапазонами чисел. Она возвращает кортеж из двух целых чисел, представляющих
    начало и конец диапазона для генерации номеров карт.

    Параметры:
    - (1, 10): Тестовый диапазон от 1 до 10, проверяет работу с малыми числами.
    - (100, 110): Тестовый диапазон от 100 до 110, проверяет работу со средними числами.
    - (99999, 99999): Тестовый диапазон с одинаковым началом и концом, проверяет работу с одним числом.

    Возвращаемое значение:
    request.param - текущий параметр из списка params, который будет использоваться в тесте.
    """
    return request.param



def test_card_number_generator(test_data):
    """
    Тест генератора номеров карт.

    Этот тест проверяет работу функции card_number_generator с различными диапазонами чисел.
    Он использует параметризацию для проверки нескольких случаев.

    :param test_data: Кортеж, содержащий начальную и конечную точки диапазона.
    """
    start, stop = test_data
    expected_output = [str(i).zfill(16) for i in range(start, stop + 1)]

    actual_output = []
    generator = card_number_generator(start, stop)
    for _ in range(len(expected_output)):
        actual_output.append(next(generator))

    assert actual_output == expected_output, f"Expected {expected_output}, got {actual_output}"


def test_start_at_16():
    """
    Тест генератора номеров карт, начинающегося с 16.

    Этот тест проверяет, правильно ли работает генератор при начале диапазона с 16.
    Он создает список из двух чисел (16 и 17) и сравнивает его с ожидаемым результатом.
    """
    output = list(card_number_generator(16, 17))
    assert output == ["0000000000000016", "0000000000000017"], "Unexpected output"


def test_stop_at_16():
    """
    Тест генератора номеров карт, заканчивающегося на 16.

    Этот тест проверяет, правильно ли работает генератор при окончании диапазона на 16.
    Он создает список из двух чисел (15 и 16) и сравнивает его с ожидаемым результатом.
    """
    output = list(card_number_generator(15, 16))
    assert output == ["0000000000000015", "0000000000000016"], "Unexpected output"


def test_range_includes_16():
    """
    Тест генератора номеров карт для диапазона, включающего число 16.

    Этот тест проверяет работу генератора в более широком диапазоне, который включает число 16.
    Он создает список из четырех чисел (14, 15, 16 и 17) и сравнивает его с ожидаемым результатом.
    """
    output = list(card_number_generator(14, 17))
    assert output == [
        "0000000000000014",
        "0000000000000015",
        "0000000000000016",
        "0000000000000017",
    ], "Unexpected output"
