import requests
import lxml.html
from datetime import datetime

'''Комментарий: 
метод /add: Принимает поисковую фразу и регион и возвращает словарь с данными {регион(
преобразованного в транслит),запрос} 
метод text_to_translite: преобразуе запрос на русском в транслит метод 
Метод  /stat: принимает на вход ловарь с данными(id) и возвращает количество объявлений(счетчики) и соответствующие им 
временные метки (timestamp). 

Задача: Необходимо реализовать сервис, позволяющий следить за изменением количества объявлений в Авито по 
определённому поисковому запросу и региону 

UI не нужен, достаточно сделать JSON API сервис.

Для написание сервиса можно использовать FastAPI или любой другой фреймворк.

Метод /add Должен принимать поисковую фразу и регион, регистрировать их в системе. Возвращать id этой пары. Метод 
/stat Принимает на вход id связки поисковая фраза + регион и интервал, за который нужно вывести счётсики. Возвращает 
счётчики и соответствующие им временные метки (timestamp). Частота опроса = 1 раз в час  для каждого id 

'''


def text_to_translite(text):
    """
    Функция преобразуюзая в транслит запрос юзера на русском, так как в url avito.ru используется именно транслит для
    определения региона
    :param text: запрос на русском
    :return: вводимый запрос в транслите
    """
    answer = ''
    russian_alphabet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ж': 'zh', 'з': 'z', 'и': 'i',
                        'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's',
                        'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
                        'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya', ' ': '_', '-': '-'}
    for i in range(len(text)):
        if text.lower()[i] in russian_alphabet:
            answer = answer + russian_alphabet[text.lower()[i]]
    return answer


class Number_of_ads_in_Avito:

    # def __init__(self, region, query):
    #     self.region = region
    #     self.query = query

    def add(self, region, query):
        """
        Функция принимает регион и поисковую фразу (на русском) и возвращает словарь с данными в виде {регион(
        преобразованного в транслит),запрос} :param region: Регион (на русском) :param query: запрос (на русском)
        :return: словарь с данными в виде {region:'регион(преобразованного в транслит)',query:'запрос'}
        """
        query_id = {'region': text_to_translite(region), 'query': query}
        return query_id

    def stat(self, query_id):
        """
        Функция принимает на вход словарь с данными(query_id) и возвращает количество объявлений(счетчики) и
        соответствующие им временные метки (timestamp).
        В headers добавлены файлы cookie, так как иначе avito.ru блокирует доступ к сайту

        :param query_id: словарь с данными в виде {region:'регион(преобразованного в транслит)',query:'запрос'}
        :return: None
        :print: количество объявлений(счетчики) и соответствующие им временные метки (timestamp)
        """
        url = f'https://www.avito.ru/{query_id["region"]}?q={query_id["query"]}'
        header = {'Accept': 'application/json, */*; q=0.01', 'accept-encoding': 'application/json, */*; q=0.01',
                  'Content-Type': 'application/json; charset=UTF-8',
                  'Cache-Control': 'no-store, no-cache, must-revalidate', 'Pragma': 'no-cache',
                  'cookie': 'u=2ke82xhf.q3xvs3.1r4rfrpkafm0; buyer_laas_location=637640; buyer_location_id=637640; ' 'luri=moskva;buyer_selected_search_radius4=0_general; ' 'sessid=966725885ac18d58be8b2fa98050584b.1606204212; ''__cfduid=d34146906e8cfa969cfa7b85f194356fe1606204212; ' 'showedStoryIds=51-50-49-48-47-46-45-43-41-42-39-32-30-25;lastViewingTime=1606204216902; ' 'no-ssr=1; _ym_uid=1606204217846271912; _ym_d=1606204217;_ga=GA1.2.2090136394.1606204218; ' '_gid=GA1.2.918753297.1606204218; _ym_isad=2; _fbp=fb.1.1606204218390.421947979;' '__gads=ID=314090f8aa02b691:T=1606204216:S=ALNI_MZtOPmE-A517HXoclAtoQn9mwfPRw; ' 'isCriteoSetNew=true; ' 'f=5''.df155a60305e515a4b5abdd419952845a68643d4d8df96e9a68643d4d8df96e9a68643d4d8df96e9a68643d4d8df96e94f9572e6986d0c624f9572e6986d0c624f9572e6986d0c62ba029cd346349f36c1e8912fd5a48d02c1e8912fd5a48d0246b8ae4e81acb9fa143114829cf33ca746b8ae4e81acb9fa46b8ae4e81acb9fae992ad2cc54b8aa8b175a5db148b56e9bcc8809df8ce07f640e3fb81381f359178ba5f931b08c66a59b49948619279110df103df0c26013a2ebf3cb6fd35a0ac91e52da22a560f550df103df0c26013a7b0d53c7afc06d0bba0ac8037e2b74f92da10fb74cac1eab71e7cb57bbcb8e0f71e7cb57bbcb8e0f71e7cb57bbcb8e0f0df103df0c26013a93e76904ac7560d30c79affd4e5f1d11162fe9fd7c8e97671096a440e86e9ad448429bdb180bc2b45e61d702b2ac73f7bbbe48e344b5827f6d85b54225227d5eeb2d4c6d5a5fa6f7990d184a24537cd0c772035eab81f5e146b8ae4e81acb9fa46b8ae4e81acb9faf5b8e78c6f0f62a38272f692e54c970ecc335e94678b63fe2da10fb74cac1eab2da10fb74cac1eabc98d1c3ab1f148dc193cc3161054d47da6ef565a9fc26059; buyer_selected_search_radius0=0; buyer_popup_location=0; view=default; _gcl_au=1.1.1703630574.1606212869; v=1606216529; _ym_visorc_34241905=b; dfp_group=50; abp=0; sx=H4sIAAAAAAACA1XQTXLCMAwF4Lt4zULEfwrHiRrUQQMCnEYBhrtXWUDpwivLn9%2FTI3Q%2FtMUIp%2B5LEqAwtEZsai3sHmEOuzAOeB5qNysxoEIjUASflKbUWMImjGG3LVC6vodSnpsQb0lpyqe9HEmcJCFjUn2LF15uqR3iIgrsjCVpgg1ExfU%2FMUKGkl2sh2l%2FL9MwHsHMRQQVNjN%2BkXxb5hQXikUZPZsiGjKY%2BqGEnyG3MYKTRe7CucTrgRKtETmZ%2BTN6kTm3Opfhes6ohH5ngh6UjX2S2yeZao9O9v7ZWCcdfYtrExRlb5je5PdpuZRLmWpP4LmY1%2FbQuDVbk%2F5bZVfT8%2FkLP710qp8BAAA%3D; so=1606218665'}
        result = requests.get(url, headers=header)
        result.raise_for_status()
        tree = lxml.html.document_fromstring(result.content)
        if query_id['query'] == '':
            news = tree.xpath('//span[@class ="category-with-counters-count-29J0p"]')
        else:
            news = tree.xpath('//span[@class="page-title-count-1oJOc"]')
        now = datetime.now()
        return (
            f'Колличество запросов "{query_id["query"]}" по региону {query_id["region"]} составляет {news[0].text}, '
            f'время {now.strftime("%d-%m-%Y %H:%M")}')


if __name__ == '__main__':
    start = Number_of_ads_in_Avito()
    print(start.stat(start.add('Архангельск', 'машина')))
