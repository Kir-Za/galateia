import string
from functools import reduce

from django.conf import settings


def get_has_prices(text) -> bool:
    """
    Есть ли цены в статье
    :return: True/False
    """
    return ('$' in text) or ('€' in text) or ('рублей' in text)


def get_has_percents(text) -> bool:
    """
    Есть ли проценты в татье
    :return: True/False
    """
    return ('%' in text) or ('процент' in text)


def get_frequent_words(text, number=10):
    """
    Получение наиболее частых слов в тексте статьи
    :param number: сколько наиболее частых слов вернуть
    :return: список слов
    """
    main_text = text.lower()
    shift_symbols = string.punctuation + string.digits + '\n' + '\t' + '\r' + '€'
    shift_table = {ord(symbol): None for symbol in shift_symbols}
    clear_text = main_text.translate(shift_table)
    text_list = clear_text.split(' ')
    frequent_words = [(text_list.count(key), key) for key in set(text_list) if key not in settings.STOP_WORDS]
    frequent_words.sort()
    if len(frequent_words) >= abs(number):
        return reduce(lambda y, x: str(y) + ', ' + str(x), [i[1] for i in frequent_words[-abs(number):]])
    return None
