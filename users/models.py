from django.contrib.auth.models import AbstractUser
from django.db import models

from sites.models import Site, Article


class UserSite(models.Model):
    """
    Конфигурирование рекомендательной системы конкретного пользователя к определенному новостному разделу.
    """
    site = models.ForeignKey(Site, on_delete=models.CASCADE, verbose_name='Корневой сайт.')
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Пользователь')
    key_words = models.TextField(max_length=500, verbose_name='Ключевое слово для поиска', default='', blank=True)
    exclude_words = models.TextField(
        max_length=500,
        verbose_name='Слова для исключающей фильтрации',
        blank=True,
        default=''
    )

    class Meta:
        unique_together = ("site", "user")

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
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Пользователь')
    user_estimation = models.CharField(
        choices=USER_ESTIMATION,
        max_length=2,
        default=SOMEHOW,
        verbose_name='Пользовательская оценка'
    )

    class Meta:
        unique_together = ("article", "user")


class User(AbstractUser):
    """
    Пользователь системы.
    """
    USER = 'ur'
    ACTOR = 'ac'

    USER_CHOICE_FIELD = (
        (USER, 'Пользователь системы'),
        (ACTOR, 'Профиль анализатора')
    )

    user_type = models.CharField(max_length=2, choices=USER_CHOICE_FIELD, default=USER, verbose_name='Тип пользователя')
    sites = models.ManyToManyField(Site, verbose_name='Пользовательские сайты', through=UserSite)
    articles = models.ManyToManyField(Article, verbose_name='Пользовательские сайты', through=UserArticle)

    class Meta:
        ordering = ['username', '-date_joined']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
