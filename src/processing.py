def filter_by_state(list_dicts: list[dict]) -> list:
    list_key_stat = []
    stste = 'EXECUTED'

    for i in list_dicts:
        if i['state'] == stste:
            list_key_stat.append(i)
        else:
            list_dicts.remove(i)



def sort_by_date(list_of_date:  list[dict[str]]) -> list:
    ''' Принимает список словарей и параметр позволяющий сортировать по дате'''
    sorted_list = sorted(list_of_date, key = lambda x: x['date'], reverse = True)

    return sorted_list
