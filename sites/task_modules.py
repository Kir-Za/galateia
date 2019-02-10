from billiard.pool import Pool

from django.conf import settings

from sites.models import Site, Article
from sites.utils import get_frequent_words, get_has_percents, get_has_prices


class RenderAndSave():
    def __init__(self, async_mode=True):
        """
        :param async_mode: False - используется для теста
        """
        self.async_mode = async_mode

    @staticmethod
    def get_available_sites(news_portal=None, news_dep=None) -> list:
        """
        Получение списка доступных сайтов
        :param news_portal: новостной портал, по активным тематическим разделам которого будет выполнен поиск, если
        не задан - поиск ведется по всем активным
        :param news_dep: новостной раздел портала
        :return: query
        """
        if news_portal:
            return [Site.objects.filter(is_active=True, news_portal=news_portal, news_department=news_dep)]
        return [site for site in Site.objects.filter(is_active=True)]

    def _save_postgr(self, results):
        """
        Сохранение в Postgresql результатов парсинга
        :param results: список с корежами, содержащими словарь, описывающий результат парсинга отдельной статьи
        :return:
        """
        for part in results:
            for result in part:
                Article.objects.get_or_create(
                    link=result['news_link'],
                    has_prices=get_has_prices(result['main_text']),
                    has_percents=get_has_percents(result['main_text']),
                    frequent_words=get_frequent_words(result['main_text']),
                    content=result
                )

    def _async_worker(self, sites_list) -> tuple:
        """
        Запуск парсера в асинхронном режиме.
        :param sites_list: список сайтов для анализа
        :return: спискок кортежей с резульатами парсинга
        """
        self.process_pool = Pool(processes=settings.PROCESS_AMOUNT)
        results = [self.process_pool.apply_async(settings.AVAILABLE_RENDERS[site.news_portal], args=(site.target_url,))
                   for site in sites_list]
        clean_data = [i.get() for i in results]
        self.process_pool.close()
        self.process_pool.join()
        return clean_data

    def _sync_worker(self, site) -> list:
        """
        Запуск парсера в синхронном режиме.
        :param sites_list: сайт для анализа
        :return: спискок кортежей с резульатами парсинга
        """
        return [settings.AVAILABLE_RENDERS[site.news_portal].__call__(site.target_url)]

    def run_parser(self) -> str:
        """
        Запуск парсера.
        :return:
        """
        if self.async_mode:
            sites_list = self.get_available_sites()
            data_from_site = self._async_worker(sites_list)
        else:
            sites_list = self.get_available_sites().pop()
            data_from_site = self._sync_worker(sites_list)
        self._save_postgr(data_from_site)
        return [i.target_url for i in sites_list]
