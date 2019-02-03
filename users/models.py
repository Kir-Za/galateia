from django.contrib.auth.models import AbstractUser
from django.db import models

from sites.models import Site


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

    class Meta:
        ordering = ['username', '-date_joined']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
