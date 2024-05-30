from django_filters import CharFilter, FilterSet, NumberFilter

from reviews.models import Title


class TitleFilter(FilterSet):
    genre = CharFilter(field_name='genre__slug')
    category = CharFilter(field_name='category__slug')
    # TODO: icontains все таки больше ориентирован на полнотекстовый поиск.
    #  При большом количестве данных он будет очень долго искать, так как в
    #  обычных СУБД мы не можем  разибвать слова на токены для индексации.
    #  Для этого существуют другие базы данных, поисковые. Например,
    #  ElasticSearch. Но это вам просто для информации) Тут лучше использовать
    #  либо iexact либо istartswith ПЫСЫ в SQLite это работать будет через пень
    #  колоду, но в серьёзных БД наподобие PostgreSQL или MySQL, которые вы скорее
    #  всего будете использовать на работе, это прекрасно работает
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
