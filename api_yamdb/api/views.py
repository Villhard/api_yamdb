from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from reviews.models import Category, Genre, Title, Review
from .serializers import CategorySerializer, GenreSerializer, ReviewSerializer, CommentSerializer
from .mixins import ListCreateDestroyViewSet
from permissions import IsOwnerOrReadOnly


class CategoryViewSet(ListCreateDestroyViewSet):
    """Представление для категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDestroyViewSet):
    """Представление для жанров"""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ReviewViewSet(ModelViewSet):
    """
    Получение одного/всех отзывов любыми пользователями.
    Добавление/обновление/удаление отзыва автором отзыва.
    """

    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    )

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
        IsOwnerOrReadOnly,
    )

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
