from rest_framework import viewsets

from reviews.models import Category, Genre
from .mixins import ListCreateDestroyViewSet
from .serializers import CategorySerializer, GenreSerializer


class CategoryViewSet(ListCreateDestroyViewSet):
    """Представление для категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDestroyViewSet):
    """Представление для жанров"""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
