from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User
from . import constants
from .validators import year_validator



class Category(models.Model):
    """Модель категории"""

    name = models.CharField('Название', max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанра"""

    name = models.CharField('Название', max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведения"""

    name = models.CharField('Название', max_length=256)
    year = models.IntegerField(
        'Год',
        validators=[
            year_validator,
        ],
        blank=True,
        null=True,
    )
    description = models.TextField('Описание', blank=True, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
        related_name='titles',
    )
    genre = models.ManyToManyField(
        Genre, blank=True, related_name='titles', verbose_name='Жанр'
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель отзыва."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Название произведения',
        related_name='reviews',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор отзыва',
        related_name='reviews',
    )
    text = models.TextField('Текст отзыва')
    score = models.IntegerField(
        'Рейтинг произведения',
        validators=[
            MinValueValidator(constants.MIN_SCORE),
            MaxValueValidator(constants.MAX_SCORE),
        ],
    )
    pub_date = models.DateTimeField(
        'Дата и время публикации отзыва', auto_now_add=True
    )

    def __str__(self):
        return self.text[:50]

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], name='unique_author_title'
            )
        ]  # На одно произведение пользователь может оставить только один отзыв
        ordering = ['-pub_date']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Comment(models.Model):
    """Модель комментария."""

    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария',
        related_name='comments',
    )
    text = models.TextField('Текст комментария')
    pub_date = models.DateTimeField(
        'Дата и время публикации комментария', auto_now_add=True
    )

    def __str__(self):
        return self.text[:50]

    class Meta:
        ordering = ['pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
