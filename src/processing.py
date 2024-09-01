
def filter_by_state(list_dicts):


    list_key_stat = []
    state = 'EXECUTED'

    for i in list_dicts:
        if i['state'] == state:
            list_key_stat.append(i)
        else:
            list_dicts.remove(i)

    return list_key_stat
print(filter_by_state([{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}, {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}, {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}, {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}]))


# def sort_by_date(list_of_date:  list[dict[str]]) -> list:
#     ''' Принимает список словарей и параметр позволяющий сортировать по дате'''
#     sorted_list = sorted(list_of_date, key = lambda x: x['date'], reverse = True)
#
#     return sorted_list
