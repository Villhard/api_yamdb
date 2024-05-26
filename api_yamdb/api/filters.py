from django_filters import CharFilter, FilterSet, NumberFilter

from reviews.models import Title


class TitleFilter(FilterSet):
    genre = CharFilter(field_name='genre__slug')
    category = CharFilter(field_name='category__slug')
    name = CharFilter(lookup_expr='icontains', field_name='name')
    year = NumberFilter(field_name='year')

    class Meta:
        model = Title
        fields = [
            'genre',
            'category',
            'name',
            'year',
        ]
