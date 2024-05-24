from rest_framework import filters, mixins, viewsets

from .permissions import IsAdminOrReadOnly


class ListCreateDestroyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    Миксин для категорий и жанров.
    Разрешенные действия:
    Получение списка всеми пользователями
    Создание и удаление только администратором.
    Поиск по полю name.
    """

    lookup_field = 'slug'
    filter_backends = [
        filters.SearchFilter,
    ]
    search_fields = [
        'name',
    ]
    permission_classes = [
        IsAdminOrReadOnly,
    ]
