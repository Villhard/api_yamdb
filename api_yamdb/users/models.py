from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Расширенная модель пользователя.

    Изменения:
    - добавлены поля bio и role
    - поле password необязательно
    """

    email = models.EmailField(unique=True)

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    roles = (
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    )
    password = models.CharField(
        'Пароль', max_length=128, blank=True, null=True
    )
    bio = models.TextField('О себе', blank=True, null=True)
    role = models.CharField(
        'Статус',
        max_length=50,
        blank=True,
        null=True,
        choices=roles,
        default='user',
    )

    def check_confirmation_code(self, code):
        """
        Проверка кода подтверждения.
        """
        return (
            self.confirmationcode.code == code
            and timezone.now() - timedelta(minutes=10)
            < self.confirmationcode.created_at
        )

    @property
    def is_admin(self):
        return self.role == User.ADMIN

    @property
    def is_moderator(self):
        return self.role == User.MODERATOR

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['id']


class ConfirmationCode(models.Model):
    """
    Модель кода подтверждения.

    user: Пользователь
    code: Код подтверждения
    created_at: Дата и время создания кода
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now=True)
