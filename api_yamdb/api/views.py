from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from reviews.models import Review
from serializers import ReviewSerializer, CommentSerializer
from permissions import IsOwnerOrReadOnly


class ReviewViewSet(ModelViewSet):
    """
    Получение одного/всех отзывов любыми пользователями.
    Добавление/обновление/удаление отзыва автором отзыва.
    """

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


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
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        serializer.save(author=self.request.user, review=review)
