import pytest

from src.decorators import log


def capsys():
    """
    Фикстура для получения объекта CaptureFixture из pytest.

    Возвращает:
    pytest.captureio.CaptureFixture: Объект для захвата вывода.

    Примечание:
    Эта функция используется для тестирования вывода, генерируемого нашими декораторами.
    """
    return pytest.captureio.CaptureFixture()


@pytest.fixture(scope="function")
def capsys_fixture(capsys):
    """
    Фикстура для удобного доступа к capsys в тестах.

    Параметры:
    capsys (pytest.captureio.CaptureFixture): Объект для захвата вывода.

    Возвращает:
    pytest.captureio.CaptureFixture: Объект для захвата вывода.

    Примечание:
    Эта фикстура позволяет легко получать вывод в наших тестах без необходимости повторно передавать capsys.
    """
    return capsys


def test_my_function(capsys_fixture):
    """
    Тест функции с декоратором log().

    Проверяем, что декоратор корректно логирует начало и конец выполнения функции,
    а также время выполнения.

    Успешный случай: функция выполняется без ошибок.
    """

    @log()
    def decorated_function(x, y):
        return x + y

    decorated_function(1, 2)

    captured = capsys_fixture.readouterr()
    assert "decorated_function started" in captured.out
    assert "decorated_function finished successfully" in captured.out
    assert "Execution time:" in captured.out


def test_my_function_with_error(capsys_fixture):
    """
    Тест функции с декоратором log(), которая выбрасывает исключение.

    Проверяем, что декоратор корректно логирует начало выполнения функции,
    обработку ошибки и время выполнения.

    Успешный случай: функция выбрасывает исключение ValueError.
    """

    @log()
    def decorated_function(x, y):
        raise ValueError("Test error")

    decorated_function(1, 2)

    captured = capsys_fixture.readouterr()
    assert "decorated_function started" in captured.out
    assert "decorated_function finished with error" in captured.out
    assert "ValueError" in captured.out
    assert "Execution time:" in captured.out


def test_my_function_with_filename(capsys_fixture):
    """
    Тест функции с декоратором log() и указанным файлом для логирования.

    Проверяем, что декоратор корректно записывает логи в указанный файл,
    включая начало выполнения функции, успешное завершение и время выполнения.

    Успешный случай: функция выполняется без ошибок.
    """

    @log(filename="test_log.txt")
    def decorated_function(x, y):
        return x + y

    decorated_function(1, 2)

    with open("test_log.txt", "r") as file:
        content = file.read()

    assert "decorated_function started" in content
    assert "decorated_function finished successfully" in content
    assert "Execution time:" in content
