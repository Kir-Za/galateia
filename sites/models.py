from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User


class Site(models.Model):
    """
    Сайт для парсинга
    """
    news_portal = models.CharField(max_length=10, verbose_name='Краткое название новостного ресурса', default='')
    news_department = models.CharField(max_length=10, verbose_name='Краткое раздела', default='')
    key_words = models.TextField(max_length=500, verbose_name='Ключевое слово для поиска', default='')
    exclude_words = models.TextField(
        max_length=500,
        verbose_name='Слова для исключающей фильтрации',
        blank=True,
        default=''
    )
    target_urls = models.URLField(verbose_name='Целевой url')
    is_active = models.BooleanField(default=True, verbose_name="Актуальный для парсинга сайт")

    def get_key_words(self) -> list:
        """
        Получение списка ключевых слов из строки.
        :return:
        """
        return self.key_words.split(', ')

    def __str__(self):
        return "{}".format(self.target_urls)

    class Meta:
        verbose_name = "Целевой сайт"
        verbose_name_plural = "Целевые сайты"


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
