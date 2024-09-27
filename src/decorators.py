import functools
import time
from datetime import datetime


def log(filename=None):
    """
    Функция-декоратор для логирования выполнения функций.
    Этот декоратор записывает информацию о начале и конце выполнения функции,
    включая время начала и конца выполнения, а также время выполнения.
    При возникновении ошибки, он также записывает информацию об этом.
    """

    def decorator(func):
        """
        Внутренний декоратор для обработки конкретной функции.
        Эта обертка сохраняет оригинальное имя функции и документацию с помощью functools.wraps().
        Она измеряет время выполнения функции и формирует сообщения о начале и конце выполнения.
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """
            Основная функция-обертка, которая выполняет саму функцию и управляет логированием.
            Эта функция измеряет время начала выполнения, формирует сообщение о начале выполнения,
            вызывает исходную функцию, обрабатывает возможные исключения, формирует сообщение о завершении
            и измеряет время окончания выполнения.
            """

            start_time = time.time()

            start_message = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | {func.__name__} started"

            if filename:
                try:
                    with open(filename, "a") as file:
                        file.write(start_message + "\n")
                except IOError:
                    print(f"Error opening file {filename}")

            else:
                print(start_message)

            try:
                result = func(*args, **kwargs)

                end_message = f"my_function ok\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | {func.__name__} finished successfully"
            except Exception as e:
                end_message = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | {func.__name__} finished with error: {type(e).__name__}"
                result = None  # Добавляем эту строку

            end_time = time.time()
            execution_time = f"Execution time: {(end_time - start_time):.4f} seconds"

            full_message = f"{end_message}\n{execution_time}"

            if filename:
                try:
                    with open(filename, "a") as file:
                        file.write(full_message + "\n")
                except IOError:
                    print(f"Error writing to file {filename}")
            else:
                print(full_message)

            return result  # Возвращаем результат

        return wrapper

    return decorator


"""
Пример использования декоратора:

@log(filename="mylog.txt")
def my_function(x, y):
    return x + y

my_function(1, 2)
"""


@log(filename="mylog.txt")
def my_function(x, y):
    return x + y

my_function(1, 2)
