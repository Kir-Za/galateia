"""
Утилиты для разбора tass.ru
"""
from requests_html import HTMLSession


def tass_news(site_url, render=True):
    """
    Первая страница новостей, динамически загружаемая через JS
    :param site_url: url с указанием подраздела, например /ekonomika
    :return: объект html
    """
    get_request = HTMLSession().get(site_url)
    if get_request.status_code == 200:
        if render:
            get_request.html.render()
        return get_request.html
    return None


def get_news_links(news_list, template):
    """
    Разбор element'ов с фильтрацией по подтеме
    :param news_list: список element'ов с новостыми заголовками и ссылками
    :param template: шаблон для определения искомой подтемы
    :return: кортеж вида (('Заголовок новости', 'url/новости'), ... )
    """
    link_list = []
    main_temlplate = template.split('/')[-1]
    for news_row in news_list:
        transitional_link = news_row.absolute_links.pop()
        title = news_row.text.split('\n')[-1]
        if main_temlplate in transitional_link:
            link_list.append((title, transitional_link))
    return tuple(link_list)


def get_news_tuple(url):
    """
    Список искомых новостей на первой странице
    :param url: целевой сайт, с указанием раздела
    :return: кортеж, содержащий заголовок новости и ее ссылку
    """
    news_list = tass_news(url)
    if news_list:
        news_list = news_list.xpath('//div[@class="news-list"]/*')
        return get_news_links(news_list, url)
    return None


def get_content(abs_url):
    """
    Получение содержимого страницы
    :param abs_url: url/новости
    :return: кортеж вида ('краткое описание', 'новостной текст')
    """
    page_content = tass_news(abs_url, False)
    if page_content:
        abstract = page_content.xpath('//div[@class="news-header__lead"]', first=True).text
        text_content = ""
        for raw in page_content.xpath('//div[@class="text-content"]/div[@class="text-block"]'):
            text_content += raw.text
        return abstract, text_content
    return None
