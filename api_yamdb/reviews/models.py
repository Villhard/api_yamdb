from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from users import User
from . import constants


class Review(models.Model):
    """Модель отзыва."""

    text = models.TextField(
        max_length=constants.MAX_LENGTH_FOR_CHARFIELD, verbose_name="Текст отзыва"
    )
    author = models.ForeignKey(
        User, verbose_name="Автор отзыва", related_name="reviews"
    )
    score = models.IntegerField(
        validators=[
            MinValueValidator(constants.MIN_SCORE),
            MaxValueValidator(constants.MAX_SCORE),
        ],
        verbose_name="Рейтинг произведения",
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name="Название произведения",
        related_name="reviews",
    )
    pub_date = models.DateTimeField(verbose_name="Дата и время публикации отзыва")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class Comment(models.Model):
    """Модель комментария."""

    text = models.TextField(
        max_length=constants.MAX_LENGTH_FOR_CHARFIELD, verbose_name="Текст комментария"
    )
    author = models.ForeignKey(
        User, verbose_name="Автор комментария", related_name="comments"
    )
    review = models.ForeignKey(Review, related_name="comments")
    pub_date = models.DateTimeField(verbose_name="Дата и время публикации комментария")

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
