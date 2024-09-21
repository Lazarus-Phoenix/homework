"""
Модуль для логирования функций.

Содержит декоратор log, который позволяет логировать выполнение функций,
их результаты, возможные ошибки и время выполнения.
"""

import functools
import time
from datetime import datetime

def log(filename=None):
    """
    Декоратор-фабрика для логирования функций.

    Args:
        filename (str): Имя файла для логирования. Если None, логи выводятся в консоль.

    Returns:
        function: Декоратор для логирования функций.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """
            Обертка для декорируемой функции.

            Args:
                *args: Неименованные аргументы.
                **kwargs: Именованные аргументы.

            Returns:
                Any: Результат выполнения декорируемой функции.
            """
            # Сохраняем время начала выполнения функции
            start_time = time.time()

            # Формируем сообщение о начале выполнения
            start_message = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | {func.__name__} started"

            # Логируем начало выполнения
            if filename:
                with open(filename, "a") as file:
                    file.write(start_message + "\n")
            else:
                print(start_message)

            try:
                # Выполняем оригинальную функцию
                result = func(*args, **kwargs)

                # Формируем сообщение о успешном завершении
                end_message = f"my_function ok \n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | {func.__name__} finished successfully"
            except Exception as e:
                # Если произошла ошибка, формируем соответствующее сообщение
                end_message = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | {func.__name__} finished with error: {type(e).__name__}"

            # Сохраняем время завершения
            end_time = time.time()

            # Вычисляем время выполнения
            execution_time = f"Execution time: {(end_time - start_time):.4f} seconds"

            # Формируем полное сообщение о завершении
            full_message = f"{end_message}\n{execution_time}"

            # Логируем информацию о завершении
            if filename:
                with open(filename, "a") as file:
                    file.write(full_message + "\n")
            else:
                print(full_message)

            # Возвращаем результат выполнения функции
            return result

        return wrapper

    return decorator

# Пример использования декоратора
@log(filename="mylog.txt")
def my_function(x, y):
    return x + y

my_function(1, 2)
