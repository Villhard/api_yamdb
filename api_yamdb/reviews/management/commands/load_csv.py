import csv
import os

from django.conf import settings
from django.core.management import BaseCommand
from reviews.models import Category, Genre, Title, GenreTitle, Review, Comment
from users.models import User


def category_create(row):
    Category.objects.get_or_create(id=row[0], name=row[1], slug=row[2])


def genre_create(row):
    Genre.objects.get_or_create(id=row[0], name=row[1], slug=row[2])


def title_create(row):
    Title.objects.get_or_create(
        id=row[0], name=row[1], year=row[2], category_id=row[3]
    )


def user_create(row):
    User.objects.get_or_create(
        id=row[0],
        username=row[1],
        email=row[2],
        role=row[3],
        bio=row[4],
        first_name=row[5],
        last_name=row[6],
    )


def review_create(row):
    # TODO: Если переменная не используется, в данном случае created,то её лучше обозначить как _
    #  https://stackoverflow.com/questions/5893163/what-is-the-purpose-of-the-single-underscore-variable-in-python
    #  Вот тут в пункте 3 описано подробнее
    title, created = Title.objects.get_or_create(id=row[1])
    Review.objects.get_or_create(
        id=row[0],
        title=title,
        text=row[2],
        author_id=row[3],
        score=row[4],
        pub_date=row[5],
    )


def comment_create(row):
    review, created = Review.objects.get_or_create(id=row[1])
    Comment.objects.get_or_create(
        id=row[0],
        review=review,
        text=row[2],
        author_id=row[3],
        pub_date=row[4],
    )


def genre_title_create(row):
    title, created = Title.objects.get_or_create(id=row[1])
    genre, created = Genre.objects.get_or_create(id=row[2])
    GenreTitle.objects.get_or_create(id=row[0], title=title, genre=genre)


actions = {
    'category.csv': category_create,
    'genre.csv': genre_create,
    'titles.csv': title_create,
    'users.csv': user_create,
    'review.csv': review_create,
    'comments.csv': comment_create,
    'genre_title.csv': genre_title_create,
}


class Command(BaseCommand):
    help = 'Load DB from CSV files'

    def handle(self, *args, **options):
        for filename in actions:
            path = os.path.join(settings.BASE_DIR, 'static/data/') + filename
            with open(path, 'r', encoding='utf-8') as file:
                csv_file = csv.reader(file)
                next(csv_file)
                for row in csv_file:
                    actions[filename](row)
        self.stdout.write('База данных загружена')
