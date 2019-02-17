from django.contrib.auth.models import AbstractUser
from django.db import models


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

    class Meta:
        ordering = ['username', '-date_joined']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
