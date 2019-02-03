import string

from django.db import models
from django.contrib.postgres.fields import JSONField
from django.conf import settings


class Site(models.Model):
    """
    Сайт для парсинга
    """
    news_portal = models.CharField(
        max_length=20,
        verbose_name='Краткое название новостного ресурса',
        default='',
        blank=True
    )
    news_department = models.CharField(max_length=10, verbose_name='Краткое имя раздела', default='', blank=True)
    target_url = models.URLField(verbose_name='Целевой url')
    is_active = models.BooleanField(default=True, verbose_name="Актуальный для парсинга сайт")

    class Meta:
        verbose_name = "Целевой сайт"
        verbose_name_plural = "Целевые сайты"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.news_portal:
            prob_list = self.target_url.strip('http').strip('s://').strip('www.').split('/')
            self.news_portal = prob_list.pop(0)
            self.news_department = prob_list[0] if prob_list else ''
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return "{}".format(self.target_url)


class Article(models.Model):
    """
    Статьи для анализа
    """
    link = models.URLField(verbose_name='Адрес', unique=True)
    content = JSONField()

    class Meta:
        indexes = [models.Index(fields=['link'])]
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"

    def __str__(self):
        return str(self.link)

    @property
    def has_prices(self) -> bool:
        """
        Есть ли цены в статье
        :return: True/False
        """
        return ('$' in self.content['main_text']) or ('€' in self.content['main_text'])

    @property
    def has_percents(self) -> bool:
        """
        Есть ли проценты в татье
        :return: True/False
        """
        return ('%' in self.content['main_text']) or ('процент' in self.content['main_text'])

    def get_frequent_words(self, number=10):
        """
        Получение наиболее частых слов в тексте статьи
        :param number: сколько наиболее частых слов вернуть
        :return: список слов
        """
        main_text = self.content['main_text'].lower()
        shift_symbols = string.punctuation + string.digits + '\n' + '\t' + '\r' + '€'
        shift_table = {ord(symbol): None for symbol in shift_symbols}
        clear_text = main_text.translate(shift_table)
        text_list = clear_text.split(' ')
        frequent_words = [(text_list.count(key), key)for key in set(text_list) if key not in settings.STOP_WORDS]
        frequent_words.sort()
        if len(frequent_words) >= abs(number):
            return frequent_words[-abs(number):]
        return None
