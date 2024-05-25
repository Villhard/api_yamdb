from rest_framework.serializers import ModelSerializer, CurrentUserDefault
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Genre, Review, Comment


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
