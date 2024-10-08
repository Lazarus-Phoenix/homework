#Тестирование 
1. Добавлены тесты модуля masks
2. Добавлены тесты модуля widget
3. Добавлены тесты модуля processing
4. Добавлены тесты модуля generators
5. Добавлены тесты модуля decorators
6. Добавлены тесты модуля utils
7. Добавлены тесты модуля external_api

# Банковские Операции: Фильтрация и Сортировка

## Описание проекта .

Этот проект предоставляет функции для обработки банковских операций:

1. Функция фильтрации по состоянию операции
2. Функция сортировки операций по дате
3. Добавлен модуль processing
4. Добавлен модуль generators
5. Добавлен модуль decorators
6. Добавлены модули utils, external_api для работы с request & JSON .

## Функциональность
Используется логирование с перезаписью только последних событий в лог.

### Фильтрация по состоянию

Функция принимает на вход список словарей с данными о банковских операциях и параметр `state`. Она возвращает новый список, содержащий только те словари, у которых ключ `state` соответствует переданному значению.

- Параметр `state` имеет значение по умолчанию `'EXECUTED'`.
- Типичный формат входных данных:
 
for python  [{'id': int, 'state': str, 'date': str}, ...]:



### Сортировка по дате

Функция принимает на вход список словарей и параметр порядка сортировки. Она возвращает новый список, в котором исходные словари отсортированы по дате.

- Параметр порядка сортировки имеет значение по умолчанию `'True'`.
- Даты сортируются в формате ISO 8601 с микросекундами.

## Использование

python from bank_operations import filter_by_state, sort_by_date

operations = [ {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}, {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}, {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}, {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'} ]

filtered_data = filter_by_state(operations) sorted_data = sort_by_date(filtered_data)

print(sorted_data)


## Установка

Для использования этого проекта:

1. Клонируйте репозиторий:

2. Перейдите в директорию проекта:

3. Создайте и активируйте виртуальное окружение Python.

4. Установите зависимости:


## Вклад в проект

Ваш вклад приветствуется! 
Пожалуйста, пишите ваши ценные предложения 
[спонсорское пожелание внесения изменений крупными купюрами]('dmitrij-bezgubov@yandex.ru').
