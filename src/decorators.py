"""
Модуль для логирования функций.

Содержит декоратор log, который позволяет логировать выполнение функций,
их результаты и возможные ошибки.
"""

import functools


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
            """@functools.wraps(func) - Сохранение имени оригинальной функции, её описи и докстринги и хелпы.
            Сохранение информации о метаданных
            Информация о модуле, где определена функция, также сохраняется
            Сохранение аннотаций типов:
            Если у оригинальной функции есть аннотации типов, они будут сохранены.
            """
            """
            Обертка для декорируемой функции.

            Args:
                *args: Неименованные аргументы.
                **kwargs: Именованные аргументы.

            Returns:
                Any: Результат выполнения декорируемой функции.
            """
            try:
                # Выполняем декорируемую функцию
                result = func(*args, **kwargs)
                # Формируем сообщение об успехе
                message = f"{func.__name__} ok"
            except Exception as e:
                # Если возникло исключение, формируем сообщение об ошибке
                message = f"{func.__name__} error: {type(e).__name__}. Inputs: {str(args)}, {str(kwargs)}"

            # Логируем сообщение
            if filename:
                # Записываем в файл
                with open(filename, "a") as file:
                    file.write(message + "\n")
            else:
                # Выводим на консоль в противном случае.
                print(message)

            # Возвращаем результат выполнения функции
            return result

        return wrapper

    return decorator


@log(filename="mylog.txt")
def my_function(x, y):
    """
    Пример функции для демонстрации работы декоратора.

    Args:
        x (int): Первое число.
        y (int): Второе число.

    Returns:
        int: Сумма двух чисел.
    """
    return x + y


# Вызов функции с логированием
result = my_function(1, 2)
print(f"Результат: {result}")