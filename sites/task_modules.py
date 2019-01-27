from billiard.pool import Pool

from django.conf import settings

from sites.models import Site, TmpContent
from sites.tass_utils import tass_circle


class RenderAndSave():
    AVAILABLE_RENDERS = {
        'tass': tass_circle,
    }

    def __init__(self, async_mode=True):
        self.async_mode = async_mode

    @staticmethod
    def get_available_sites(news_portal=None, news_dep=None) -> list:
        """
        Получение списка доступных сайтов
        :param news_portal: новостной портал, по активным тематическим разделам которого будет выполнен поиск, если
        не задан - поиск ведется по всем активным
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
                if not TmpContent.objects.filter(link=result['news_link']).first():
                    key_words = Site.objects.filter(target_urls=result['target']).first().get_key_words()
                    for key in key_words:
                        if key in result['news_title']:
                            TmpContent.objects.create(
                                target_site=result['target'],
                                link=result['news_link'],
                                title=result['news_title'],
                                abstract=result['abstract'],
                                body=result['main_text']
                            )
                            break

    def _async_worker(self, sites_list) -> tuple:
        """
        Запуск парсера в асинхронном режиме.
        :param sites_list: список сайтов для анализа
        :return: спискок кортежей с резульатами парсинга
        """
        #self.process_pool = mp.Pool(processes=settings.PROCESS_AMOUNT)
        self.process_pool = Pool(processes=settings.PROCESS_AMOUNT)
        results = [self.process_pool.apply_async(self.AVAILABLE_RENDERS[site.news_portal], args=(site.target_urls,))
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
        site = site[0]
        return [self.AVAILABLE_RENDERS[site.news_portal].__call__(site.target_urls)]

    def run_parser(self) -> str:
        """
        Запуск парсера.
        :return:
        """
        if self.async_mode:
            sites_list = self.get_available_sites()
            data_from_site = self._async_worker(sites_list)
        else:
            single_site = self.get_available_sites(news_portal='tass', news_dep='ekonomika').pop()
            data_from_site = self._sync_worker(single_site)
        self._save_postgr(data_from_site)
