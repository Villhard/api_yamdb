from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import (
    CurrentUserDefault,
    IntegerField,
    ModelSerializer,
    ValidationError,
)
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Genre, Review, Comment, Title


class CategorySerializer(ModelSerializer):
    """Сериализатор для категорий."""

    class Meta:
        model = Category
        exclude = [
            'id',
        ]


class GenreSerializer(ModelSerializer):
    """Сериализатор для жанров."""

    class Meta:
        model = Genre
        exclude = [
            'id',
        ]


class TitleSerializer(ModelSerializer):
    """Сериализатор для произведений."""

    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'

    def validate_year(self, value):
        if value > timezone.now().year:
            raise ValidationError('Не корректный год!')
        return value

    def validate_genre(self, value):
        if not Genre.objects.filter(slug=value).exists():
            raise ValidationError('Нет такого жанра!')
        return value

    def validate_category(self, value):
        if not Category.objects.filter(slug=value).exists():
            raise ValidationError('Нет такой категории!')
        return value


class ReviewSerializer(ModelSerializer):
    """Сериализатор отзыва."""

    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=CurrentUserDefault(),
    )

    class Meta:
        model = Review
        exclude = [
            'title',
        ]
        read_only_fields = ('id', 'title', 'pub_date', 'author')

    def score_validate(self, score):
        if not 1 <= score <= 10:
            raise ValidationError('Оценка должна быть в диапазоне от 1 до 10.')
        return score

    # def validate(self, data):
    #     author = data.get('author')
    #     title = data.get('title')
    #     if Review.objects.filter(author=author, title=title).exists():
    #         raise ValidationError('нельзя 2')
    #     return data


class CommentSerializer(ModelSerializer):
    """Сериализатор комментария."""

    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=CurrentUserDefault(),
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('id', 'review', 'pub_date', 'author')
