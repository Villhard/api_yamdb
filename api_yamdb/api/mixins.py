from rest_framework import filters, mixins, viewsets

from api.permissions import IsAdminOrReadOnly


# TODO: Так как технически это все таки viewset,
#  то и модуль нужно переименовать из mixins.py
class ListCreateDestroyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    # TODO: Для каких моделей это миксин можно не писать.
    #  Ведь потом это может поменяться и надо будет помнить,
    #  что нужнои коммент изменить
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
