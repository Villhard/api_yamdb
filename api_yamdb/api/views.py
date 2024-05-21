from rest_framework import viewsets

from reviews.models import Category
from .mixins import ListCreateDestroyViewSet
from .serializers import CategorySerializer


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
