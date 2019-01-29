"""
Утилиты для разбора tass.ru
"""
import logging
from requests_html import HTMLSession

from sites.models import Article

logger = logging.getLogger('tmp_develop')


def tass_news(site_url, render=True):
    """
    Первая страница новостей, динамически загружаемая через JS
    :param site_url: url с указанием подраздела, например /ekonomika
    :return: объект html
    """
    try:
        get_request = HTMLSession().get(site_url)
        if get_request.status_code == 200:
            if render:
                get_request.html.render()
            return get_request.html
        logger.info("Сайт {0} вернул статус {1}".format(site_url, get_request.status_code))
        return None
    except Exception as err:
        logger.error(err.__str__())


def get_news_links(news_list, template) -> tuple:
    """
    Разбор element'ов с фильтрацией по подтеме
    :param news_list: список element'ов с новостыми заголовками и ссылками
    :param template: шаблон для определения искомой подтемы
    :return: кортеж вида (('Заголовок новости', 'url/новости'), ... )
    """
    link_list = []
    main_temlplate = template.split('/')[-1]
    try:
        for news_row in news_list:
            transitional_link = news_row.absolute_links.pop()
            title = news_row.text.split('\n')[-1]
            if main_temlplate in transitional_link:
                link_list.append((title, transitional_link))
        return tuple(link_list)
    except Exception as err:
        logger.error(err.__str__())


def get_news_tuple(url) -> tuple:
    """
    Список искомых новостей на первой странице
    :param url: целевой сайт, с указанием раздела
    :return: кортеж, содержащий заголовок новости и ее ссылку
    """
    news_list = tass_news(url)
    if news_list:
        try:
            news_list = news_list.xpath('//div[@class="news-list"]/*')
            return get_news_links(news_list, url)
        except Exception as err:
            logger.error(err.__str__())
    return tuple()


def get_content(abs_url) -> tuple:
    """
    Получение содержимого страницы
    :param abs_url: url/новости
    :return: кортеж вида ('краткое описание', 'новостной текст')
    """
    page_content = tass_news(abs_url, False)
    if page_content:
        try:
            abstract = page_content.xpath('//div[@class="news-header__lead"]', first=True).text
            text_content = ""
            for raw in page_content.xpath('//div[@class="text-content"]/div[@class="text-block"]'):
                text_content += raw.text
            return abstract, text_content
        except Exception as err:
            logger.error(err.__str__())
    return tuple()


def tass_circle(target_site) -> tuple:
    """
    Основной цикл получения списка последних неовостей и их содержания с tass.ru
    :param target_site: в данном случае tass.ru
    :return: кортеж последних новостей
    """
    news_raw = []
    site_topics = get_news_tuple(target_site)
    for topic in site_topics:
        abstract, main_text = get_content(topic[1])
        news_raw.append({
            'target': target_site,
            'news_title': topic[0],
            'news_link': topic[1],
            'abstract': abstract,
            'main_text': main_text
        })
    return tuple(news_raw)
