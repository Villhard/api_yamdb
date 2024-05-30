from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.serializers import (
    CurrentUserDefault,
    IntegerField,
    ModelSerializer,
)
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Genre, Review, Comment, Title
from reviews.constants import MIN_SCORE, MAX_SCORE


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
        # TODO: Cледуя принципу "явное лучше неявного" на мой взгляд лучше перечислить все поля,
        #  чем писать all. Например завтра добавят новое поле в модель, которое не должно выдаваться
        #  обычному юзеру, например заметка о пользователе в системе сервисдеск, или те же платежные
        #  данные, адрес и потом это утечет куда нибудь по недосмотру
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
        fields = ('id', 'author', 'text', 'score', 'pub_date')
        read_only_fields = ('id', 'title', 'pub_date', 'author')

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs['title_id']
        title = get_object_or_404(Title, id=title_id)
        if (
            request.method == 'POST'
            and Review.objects.filter(title=title, author=author).exists()
        ):
            raise ValidationError(
                'Вы уже оставляли отзыв на это произведение.'
            )
        return data

    def score_validate(self, score):
        if not MIN_SCORE <= score <= MAX_SCORE:
            raise ValidationError('Оценка должна быть в диапазоне от 1 до 10.')
        return score


class CommentSerializer(ModelSerializer):
    """Сериализатор комментария."""

    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=CurrentUserDefault(),
    )

    class Meta:
        model = Comment
        fields = ('id', 'review', 'author', 'text', 'pub_date')
        read_only_fields = ('id', 'review', 'pub_date', 'author')
