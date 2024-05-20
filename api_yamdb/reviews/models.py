from django.db import models


class Category(models.Model):
    name = models.CharField(
        "Название",
        max_length=256
    )
    slug = models.SlugField(
        max_length=50,
        unique=True
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        "Название",
        max_length=256
    )
    slug = models.SlugField(
        max_length=50,
        unique=True
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        "Название",
        max_length=256
    )
    year = models.IntegerField(
        "Год",
        blank=True,
        null=True
    )
    description = models.TextField(
        "Описание",
        blank=True,
        null=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Категория",
        related_name="titles"
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        related_name="titles",
        verbose_name="Жанр"
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
