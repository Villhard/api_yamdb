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


class ConfirmationCode(models.Model):
    """
    Модель кода подтверждения.

    user: Пользователь
    code: Код подтверждения
    created_at: Дата и время создания кода
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=16)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=True)
