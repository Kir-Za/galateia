from django.db import models


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


class TmpContent(models.Model):
    """
    Временное хранилище полученного контента, по мере введения MongoDB удалить.
    """
    target_site = models.URLField(verbose_name='Корневой сайт')
    link = models.URLField(verbose_name='Адрес')
    title = models.CharField(max_length=200, verbose_name='Заголовок', default='')
    abstract = models.TextField(verbose_name="Краткое описание", default='')
    body = models.TextField(verbose_name="Тело статьи", default='')

    def __str__(self):
        return "{}".format(self.title)
