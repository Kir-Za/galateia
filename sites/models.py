from django.db import models


class Site(models.Model):
    """
    Сайт для парсинга
    """
    key_word = models.CharField(max_length=50, verbose_name='Ключевое слово для поиска')
    support_word = models.CharField(
        max_length=50,
        verbose_name='Вспомогательное слово для поиска',
        blank=True,
        default=''
    )
    target_urls = models.URLField(verbose_name='Целевой url')
    is_active = models.BooleanField(default=True, verbose_name="Актуальный для парсинга сайт")

    def __str__(self):
        return "{} in {}".format(self.key_word, self.target_urls)

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
