from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from reviews.models import Category, Genre, Title, Review
from api.filters import TitleFilter
from api.permissions import (
    IsAdminOrReadOnly,
    IsOwnerModeratorAdminSuperuserOrReadOnly,
)
from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    ReviewSerializer,
    CommentSerializer,
)
from api.viewsets import ListCreateDestroyViewSet


class CategoryViewSet(ListCreateDestroyViewSet):
    """Представление для категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDestroyViewSet):
    """Представление для жанров"""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(ModelViewSet):
    """
    Получение списка произведений, информации о произведении,
    частичное обновление информации о произведении,
    удаление произведения.
    """

    http_method_names = ['get', 'post', 'delete', 'patch']
    serializer_class = TitleSerializer
    permission_classes = [
        IsAdminOrReadOnly,
    ]
    filter_backends = [
        DjangoFilterBackend,
    ]
    filterset_class = TitleFilter

    def get_queryset(self):
        queryset = (
            Title.objects.all()
            .annotate(rating=Avg('reviews__score'))
            .order_by('rating')
        )
        return queryset

    def perform_create(self, serializer):
        category = get_object_or_404(
            Category, slug=self.request.data.get('category')
        )
        genre = Genre.objects.filter(
            slug__in=self.request.data.getlist('genre')
        )
        serializer.save(category=category, genre=genre)

    def perform_update(self, serializer):
        self.perform_create(serializer)


class ReviewViewSet(ModelViewSet):
    """
    Получение одного/всех отзывов любыми пользователями.
    Добавление/обновление/удаление отзыва автором отзыва.
    """

    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsOwnerModeratorAdminSuperuserOrReadOnly,
    )
    http_method_names = ['get', 'post', 'patch', 'head', 'delete']

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(ModelViewSet):
    """
    Получение одного/всех комментариев любыми пользователями.
    Добавление/обновление/удаление комментария автором комментария.
    """

    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsOwnerModeratorAdminSuperuserOrReadOnly,
    )
    http_method_names = ['get', 'post', 'patch', 'head', 'delete']

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
