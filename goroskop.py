import time
import requests
import re
from bs4 import BeautifulSoup

URL = 'https://ria.ru/20200816/1575800837.html'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/99.0.4844.51 Safari/537.36'}


def get_dom_data(url=URL):
    # ConnectionResetError
    for response in range(3):
        try:
            request = requests.get(url, headers=HEADERS)
            if str(request.status_code)[0] == '4':
                print('Ошибка клиента')
                exit()
            elif str(request.status_code)[0] == '5':
                print('Ошибка сервера')
                exit()
            else:
                dom_data = BeautifulSoup(request.content, 'html.parser')
                return dom_data
        except:
            print('Соединение не установлено.')
            time.sleep(5)
    exit()


def get_regex(word):
    word_forms = (
        r'ов(?:ен|на)',
        r'тел(?:ец|ьцы)',
        r'близнец(?:ы)',
        r"рак(?:и|ах)?",
        r"л(?:ев|ьвы)",
        r"дев(?:а|ы)?",
        r"вес(?:ы|ов)",
        r"скорпион(?:ы)?",
        r'стрел(?:ец|ьцы|ьца|ьцам)',
        r'козерог(?:и|а|ов)?',
        r'водоле(?:й|и)',
        r'рыб(?:ы|а)'
    )

    for word_form in word_forms:
        if re.search(word_form, word):
            return word_form
    print('Вы ввели несуществующий знак.')
    exit()


def get_text(input_word):
    regex = get_regex(input_word)
    dom_data = get_dom_data()
    items = dom_data.find('div', class_='article__body js-mediator-article mia-analytics').find_all('div',
                                                                                                    class_='article__text')

    for facts_of_signs in items:
        if re.search(regex, facts_of_signs.get_text().lower()):
            print(facts_of_signs.get_text().lower())
    return None


signs = input('Введите свой знак зодиака: ')
get_text(signs)