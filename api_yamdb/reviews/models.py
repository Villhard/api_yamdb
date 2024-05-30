from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# TODO: Правильнее в settings.py обозначить какая модель User является
#  стандартной и везде использовать get_user_model
#  https://docs.djangoproject.com/en/5.0/ref/settings/#auth-user-model
#  https://docs.djangoproject.com/en/5.0/topics/auth/customizing/#referencing-the-user-model
from users.models import User

# TODO: Тут вы используете относителньный импорт, а выше - users.models абсолютный.
#  Вот, нужно выбрать какой-либо один способ. Для небольших проектов лучше использовать
#  абсолютные импорты https://stackabuse.com/relative-vs-absolute-imports-in-python/
from reviews.constants import MIN_SCORE, MAX_SCORE
from reviews.validators import year_validator


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
    # TODO: А почему бы нам не добавить тут индексы? Не знаю, всем ли я писал это в прошлых спринтах,
    #  поэтому повторю. Наверняка мы часто будем фильровать Title по году. Это значит, что каждый раз,
    #  база данных будет проходиться по всем произведениям по порядку пока не найдёт нужное.
    #  Для облегчения поиска добавим индекс - https://docs.djangoproject.com/en/2.2/ref/models/options/#indexes.
    #  Если кратко, то таким образом БД будет хранить наши данные упорядоченно и мы будем искать наши данные в
    #  log2 быстрее, чем без него :) Это довольно обширная тема, возможно вам будет интересно.
    #  https://im-cloud.ru/blog/chto-takoe-indeksy-bazy-dannyh-dlja-nachinajushhih/ Но стоит учесть,
    #  что их производительность не достается бесплатно. Они занимают больше места на диске и также мы уменьшаем
    #  нашу скорость записи в БД, так как на каждую запись нужно будет перестраивать индекс
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
