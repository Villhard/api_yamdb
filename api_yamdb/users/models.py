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
    roles = (
        # TODO: Лучше строки названия ролей admin, moderator, user вынести в константу внутри класса.
        #  Эти константы мы будем использовать для сравнения ролей пользователя
        #  Так мы сможем обращаться к этим константам через User.USER и тп
        ('user', 'Пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор'),
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
    # TODO: А еще модель можно расширить кастомными методами для проверки роли пользователя - is_admin, is_moderator.
    #  Так нам проще будет получать permission пользователя Лучше это сделать с использованием декоратора property

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


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
