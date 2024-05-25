from django.utils import timezone

from rest_framework.serializers import (
    CurrentUserDefault,
    FloatField,
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

    genre = GenreSerializer(read_only=True)
    category = CategorySerializer(many=True, read_only=True)
    rating = FloatField(read_only=True)

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
        fields = '__all__'
        read_only_fields = ('id', 'title', 'pub_date', 'author')


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
