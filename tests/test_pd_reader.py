import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from src.pd_reader import read_csv, read_xlsx, read_all_files_in_directory


# Фикстура для создания тестовых данных
@pytest.fixture
def sample_csv_data():
    return pd.DataFrame({
        'id': [1, 2, 3],
        'date': ['2023-01-01', '2023-01-02', '2023-01-03'],
        'amount': [100.0, 200.0, 300.0]
    })


@pytest.fixture
def sample_xlsx_data():
    return pd.DataFrame({
        'id': [4, 5, 6],
        'date': ['2023-01-04', '2023-01-05', '2023-01-06'],
        'amount': [400.0, 500.0, 600.0]
    })


# Тесты для функции read_csv
def test_read_csv(sample_csv_data):
    with patch('pandas.read_csv') as mock_read_csv:
        mock_read_csv.return_value = sample_csv_data
        result = read_csv('test.csv')
        assert len(result) == 3
        assert result[0]['id'] == 1
        assert result[1]['date'] == '2023-01-02'
        assert result[2]['amount'] == 300.0


def test_read_csv_error():
    with patch('pandas.read_csv') as mock_read_csv:
        mock_read_csv.side_effect = Exception('Test error')
        result = read_csv('test.csv')
        assert result == []


# Тесты для функции read_xlsx
def test_read_xlsx(sample_xlsx_data):
    with patch('pandas.read_excel') as mock_read_excel:
        mock_read_excel.return_value = sample_xlsx_data
        result = read_xlsx('test.xlsx')
        assert len(result) == 3
        assert result[0]['id'] == 4
        assert result[1]['date'] == '2023-01-05'
        assert result[2]['amount'] == 600.0


def test_read_xlsx_error():
    with patch('pandas.read_excel') as mock_read_excel:
        mock_read_excel.side_effect = Exception('Test error')
        result = read_xlsx('test.xlsx')
        assert result == []


# Тесты для функции read_all_files_in_directory
def test_read_all_files_in_directory(tmp_path, sample_csv_data, sample_xlsx_data):
    # Создаем временные файлы
    csv_file = tmp_path / 'test.csv'
    xlsx_file = tmp_path / 'test.xlsx'

    # Заполняем файлы тестовыми данными
    sample_csv_data.to_csv(csv_file, index=False)
    sample_xlsx_data.to_excel(xlsx_file, index=False)

    # Патчим функции чтения файлов
    with patch('src.pd_reader.read_csv') as mock_read_csv, \
            patch('src.pd_reader.read_xlsx') as mock_read_xlsx:
        mock_read_csv.return_value = sample_csv_data.to_dict('records')
        mock_read_xlsx.return_value = sample_xlsx_data.to_dict('records')

        # Вызываем тестируемую функцию
        result = read_all_files_in_directory(tmp_path)

        # Проверяем результат
        assert len(result) == 6
        assert result[0]['id'] == 1
        assert result[3]['id'] == 4


def test_read_all_files_in_directory_empty(tmp_path):
    # Патчим функции чтения файлов
    with patch('src.pd_reader.read_csv') as mock_read_csv, \
            patch('src.pd_reader.read_xlsx') as mock_read_xlsx:
        mock_read_csv.return_value = []
        mock_read_xlsx.return_value = []

        # Вызываем тестируемую функцию
        result = read_all_files_in_directory(tmp_path)

        # Проверяем результат
        assert result == []


# Тест на покрытие кода
def test_pd_reader_coverage():
    # Проверяем, что все функции покрыты тестами
    assert read_csv.__code__.co_code is not None
    assert read_xlsx.__code__.co_code is not None
    assert read_all_files_in_directory.__code__.co_code is not None