from django.db import models
from django.contrib.postgres.fields import JSONField
from users.models import User


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
    users = models.ManyToManyField(User, verbose_name='Пользовательские сайты', through='sites.UserSite')

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
    users =  models.ManyToManyField(User, verbose_name='Пользовательские сайты', through='sites.UserArticle')
    content = JSONField()

    class Meta:
        indexes = [models.Index(fields=['link'])]
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"

    def __str__(self):
        return str(self.link)


class UserSite(models.Model):
    """
    Конфигурирование рекомендательной системы конкретного пользователя к определенному новостному разделу.
    """
    site = models.ForeignKey(Site, on_delete=models.CASCADE, verbose_name='Корневой сайт.')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    key_words = models.TextField(max_length=500, verbose_name='Ключевое слово для поиска', default='', blank=True)
    exclude_words = models.TextField(
        max_length=500,
        verbose_name='Слова для исключающей фильтрации',
        blank=True,
        default=''
    )

    def __str__(self):
        return str(self.site)

    class Meta:
        unique_together = ("site", "user")
        verbose_name = "Инфо ресурс"
        verbose_name_plural = "Инфо ресурсы"

    @property
    def get_key_words(self) -> list:
        """
        Получение списка ключевых слов из строки.
        :return:
        """
        return self.key_words.split(', ')

    @property
    def get_exclude_words(self) -> list:
        """
        Получение списка ключевых слов из строки.
        :return:
        """
        return self.exclude_words.split(', ')


class UserArticle(models.Model):
    """
    Оценка статьи
    """
    SOMEHOW = 'sh'
    VERY_BAD = 'vb'
    BAD = 'bd'
    HARDLY = 'hd'
    AVERAGE = 'av'
    WELL = 'wl'
    GOOD = 'gd'
    VERY_GOOD = 'vg'

    USER_ESTIMATION = (
        (SOMEHOW, 'Без оценки'),
        (VERY_BAD, 'Раздражающая статья'),
        (BAD, 'Совсем неинтересно'),
        (HARDLY, 'Неинтересно'),
        (AVERAGE, 'Средне'),
        (WELL, 'Можно почитать'),
        (GOOD, 'Хорошая статья'),
        (VERY_GOOD, 'Очень интересно')
    )

    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья.')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    user_estimation = models.CharField(
        choices=USER_ESTIMATION,
        max_length=2,
        default=SOMEHOW,
        verbose_name='Пользовательская оценка'
    )

    class Meta:
        unique_together = ("article", "user")
        verbose_name = "Пользовательская оценка"
        verbose_name_plural = "Пользовательские оценки"
