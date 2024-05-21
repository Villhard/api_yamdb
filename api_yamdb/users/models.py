from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Расширенная модель пользователя.

    Изменения:
    - добавлены поля bio и role
    - поле password необязательно
    """

    roles = (
        ('user', 'Пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор'),
    )
    password = models.CharField(max_length=128, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    role = models.CharField(
        max_length=50, blank=True, null=True, choices=roles, default='user'
    )
