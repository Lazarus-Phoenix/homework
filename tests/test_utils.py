import pytest
import logging
import os
import json
import tempfile
from src.utils import read_transactions_from_json, transaction_amount, get_exchange_rate

@pytest.fixture(scope="session", autouse=True)
def setup_logging():
    # Создаем директорию для логов в директории tests
    log_dir = os.path.join(os.path.dirname(__file__), "logs")
    os.makedirs(log_dir, exist_ok=True)
    
    # Устанавливаем уровень логирования
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    # Создаем файловый обработчик
    file_handler = logging.FileHandler(os.path.join(log_dir, "log_utils.log"))
    file_handler.setLevel(logging.DEBUG)
    
    # Создаем форма��тер
    formatter = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s")
    file_handler.setFormatter(formatter)
    
    # Добавляем обработчик к логгеру
    logger.addHandler(file_handler)
    
    yield
    
    # Очищаем логи после завершения тестов
    logger.handlers.clear()

@pytest.fixture
def sample_json_file(tmp_path):
    test_file_path = tempfile.mkstemp()[1]
    test_data = [
        {"date": "2023-01-01", "amount": 100.0, "type": "income"},
        {"date": "2023-01-02", "amount": -50.0, "type": "expense"}
    ]
    with open(test_file_path, "w") as f:
        json.dump(test_data, f)
    return test_file_path

def test_read_transactions_from_json(sample_json_file):
    operations = read_transactions_from_json(sample_json_file)
    assert isinstance(operations, list)
    assert len(operations) == 2
    assert operations[0]["date"] == "2023-01-01"
    assert operations[0]["amount"] == 100.0
    assert operations[1]["date"] == "2023-01-02"
    assert operations[1]["amount"] == -50.0

def test_read_transactions_from_json_empty_file(tmp_path):
    empty_file_path = tempfile.mkstemp()[1]
    with open(empty_file_path, "w") as f:
        json.dump([], f)
    operations = read_transactions_from_json(empty_file_path)
    assert operations == []

def test_read_transactions_from_json_invalid_json(tmp_path):
    invalid_json_file_path = tempfile.mkstemp()[1]
    with open(invalid_json_file_path, "w") as f:
        f.write("{")
    operations = read_transactions_from_json(invalid_json_file_path)
    assert operations == []

@pytest.fixture
def sample_transactions():
    return [
        {
            'id': 1,
            'operationAmount': {
                'amount': '100',
                'currency': {'code': 'RUB'}
            }
        },
        {
            'id': 2,
            'operationAmount': {
                'amount': '50',
                'currency': {'code': 'USD'}
            }
        },
        {
            'id': 3,
            'operationAmount': {
                'amount': '75',
                'currency': {'code': 'EUR'}
            }
        }
    ]

@pytest.fixture
def mock_get_exchange_rate(monkeypatch):
    def mock_get_exchange_rate(currency):
        rates = {
            'USD': 60.0,
            'EUR': 65.0
        }
        return rates.get(currency, 1.0)
    monkeypatch.setattr('src.utils.get_exchange_rate', mock_get_exchange_rate)

def test_transaction_amount(sample_transactions, mock_get_exchange_rate):
    rub_amount, usd_amount, eur_amount = transaction_amount(sample_transactions[0])
    assert rub_amount == 100
    assert round(usd_amount, 2) == 1.67
    assert round(eur_amount, 2) == 1.54

def test_transaction_amount_usd(sample_transactions, mock_get_exchange_rate):
    rub_amount, usd_amount, eur_amount = transaction_amount(sample_transactions[1])
    assert rub_amount == 3000
    assert usd_amount == 50
    assert round(eur_amount, 2) == 46.15

def test_transaction_amount_eur(sample_transactions, mock_get_exchange_rate):
    rub_amount, usd_amount, eur_amount = transaction_amount(sample_transactions[2])
    assert rub_amount == 4875
    assert usd_amount == 81.25
    assert eur_amount == 75

def test_transaction_amount_unknown_currency(sample_transactions, mock_get_exchange_rate):
    sample_transactions.append({
        'id': 4,
        'operationAmount': {
            'amount': '100',
            'currency': {'code': 'GBP'}
        }
    })
    rub_amount, usd_amount, eur_amount = transaction_amount(sample_transactions[3])
    assert rub_amount == 0
    assert usd_amount == 0
    assert eur_amount == 0
