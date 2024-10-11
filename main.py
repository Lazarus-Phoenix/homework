#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.csv_reader import read_csv
from src.processing import count_operations_by_category, filter_by_description, filter_by_state, sort_by_date
from src.utils import read_transactions_from_json
from src.xlsx_reader import read_xlsx


def main():
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакций из JSON-файла")
    print("2. Получить информацию о транзакций из CSV-файла")
    print("3. Получить информацию о транзакций из XLSX-файла")

    choice = input("Введите номер пункта меню: ")

    if choice == "1":
        operations = read_transactions_from_json()
        print("Для обработки выбран JSON-файл.")
        print(f"Загружено {len(operations)} операций.")
    elif choice == "2":
        try:
            operations = read_csv()
            print("Для обработки выбран CSV-файл.")
            print(f"Загружено {len(operations)} операций.")
        except Exception as e:
            print(f"Ошибка при чтении CSV-файла: {str(e)}")
            return
    elif choice == "3":
        try:
            operations = read_xlsx()
            print("Для обработки выбран XLSX-файл.")
            print(f"Загружено {len(operations)} операций.")
        except Exception as e:
            print(f"Ошибка при чтении XLSX-файла: {str(e)}")
            return
    else:
        print("Некорректный выбор. Завершение программы.")
        return

    if not operations:
        print("Не найдено ни одной транзакции, подходящей под ваши условия филь��рации")
        return

    # Фильтрация по статусу
    while True:
        state = input(
            "Введите статус, по которому необходимо выполнить фильтрацию. "
            "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\n"
        ).upper()
        if state in ["EXECUTED", "CANCELED", "PENDING"]:
            break
        print("Статус операции недоступен.")

    filtered_operations = filter_by_state(operations, state)
    print(f"Операции отфильтрованы по статусу '{state}'. Загружено {len(filtered_operations)} операций.")

    # Сортировка по дате
    sort_by_date_flag = input("Отсортировать операции по дате? Да/Нет\n").lower() == "да"
    if sort_by_date_flag:
        sort_ascending = input("Отсортировать по возрастанию или по убыванию? \n").lower() == "по возрастанию"
        filtered_operations = sort_by_date(filtered_operations, reverse=not sort_ascending)

    # Фильтрация по валюте
    filter_by_rub = input("Выводить только рублевые транзакции? Да/Нет\n").lower() == "да"
    if filter_by_rub:
        filtered_operations = [
            op for op in filtered_operations if op.get("operationAmount", {}).get("currency", {}).get("code") == "RUB"
        ]

    # Фильтрация по описанию
    filter_by_description_flag = (
        input("Отфильтровать список транзакций по определенному слову в описании? Да/Нет\n").lower() == "да"
    )
    if filter_by_description_flag:
        search_string = input("Введите слово для поиска: ")
        filtered_operations = filter_by_description(filtered_operations, search_string)

    # Вывод результатов
    if not filtered_operations:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
    else:
        print(f"Всего банковских операций в выборке: {len(filtered_operations)}")
        for op in filtered_operations:
            date = op.get("date", "")
            description = op.get("description", "")
            amount = op.get("operationAmount", {}).get("amount", "0")
            currency = op.get("operationAmount", {}).get("currency", {}).get("code", "RUB")
            from_account = op.get("from", "")
            to_account = op.get("to", "")

            print(f"Дата: {date}")
            print(f"Описание: {description}")
            print(f"Сумма: {amount} {currency}")
            print(f"Счет: {from_account} -> {to_account}")
            print()

    category_counts = count_operations_by_category(filtered_operations)
    print("Категории операций и их количество:")
    for category, count in category_counts.items():
        print(f"{category}: {count}")


if __name__ == "__main__":
    main()
