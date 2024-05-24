from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework import serializers

from reviews.models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""

    class Meta:
        model = Category
        exclude = [
            'id',
        ]


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""

    class Meta:
        model = Genre
        exclude = [
            'id',
        ]


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для произведений."""

    genre = GenreSerializer(read_only=True)
    category = CategorySerializer(many=True, read_only=True)
    rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'

    def validate_year(value):
        if value > timezone.now().year:
            raise serializers.ValidationError('Не корректный год!')
        return value

    def validate_genre(value):
        if not Genre.objects.filter(slug=value).exists():
            raise serializers.ValidationError('Нет такого жанра!')
        return value

    def validate_category(value):
        if not Category.objects.filter(slug=value).exists():
            raise serializers.ValidationError('Нет такой категории!')
        return value
