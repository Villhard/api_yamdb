from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model
from django.db import models

from reviews.constants import MIN_SCORE, MAX_SCORE
from reviews.validators import year_validator


User = get_user_model()


class Category(models.Model):
    """Модель категории"""

    name = models.CharField('Название', max_length=256)
    slug = models.SlugField('Слаг', max_length=50, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанра"""

    name = models.CharField('Название', max_length=256)
    slug = models.SlugField('Слаг', max_length=50, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

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
        Genre,
        through='GenreTitle',
        related_name='titles',
        verbose_name='Жанр',
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        indexes = [
            models.Index(
                fields=[
                    'year',
                ],
                name='year_idx',
            )
        ]

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='titles',
        verbose_name='Произведение',
    )
    genre = models.ForeignKey(
        Genre,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='genres',
        verbose_name='Жанр',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'genre'], name='unique_fields_genretitle'
            )
        ]

    def __str__(self):
        return f'{self.title.name} / {self.genre.name}'


class Review(models.Model):
    """Модель отзыва."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
        related_name='reviews',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор отзыва',
        related_name='reviews',
    )
    text = models.TextField('Текст отзыва')
    score = models.PositiveSmallIntegerField(
        'Рейтинг',
        validators=[
            MinValueValidator(MIN_SCORE),
            MaxValueValidator(MAX_SCORE),
        ],
    )
    pub_date = models.DateTimeField(
        'Дата и время публикации отзыва', auto_now_add=True
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=['author', 'title'], name='unique_author_title'
            ),
        )
        ordering = ['-pub_date']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text[:50]


class Comment(models.Model):
    """Модель комментария."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
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

    class Meta:
        ordering = ['pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:50]
