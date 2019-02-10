from django.db import models
from django.contrib.postgres.fields import JSONField



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
    has_percents = models.BooleanField(default=False, verbose_name='Проценты в статье.')
    has_prices = models.BooleanField(default=False, verbose_name='Цены.')
    frequent_words = models.CharField(max_length=500, default='', verbose_name='Наиболее частыне слова.')
    content = JSONField()

    class Meta:
        indexes = [models.Index(fields=['link'])]
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"

    def __str__(self):
        return str(self.link)
