from django.utils import timezone

from django.core.exceptions import ValidationError


def year_validator(value):
    if value > timezone.now().year:
        raise ValidationError('Не корректный год!')
