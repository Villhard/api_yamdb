# Проект «YaMDb»
![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![Markdown](https://img.shields.io/badge/markdown-%23000000.svg?style=for-the-badge&logo=markdown&logoColor=white)

## Описание проекта
Проект YaMDb собирает отзывы пользователей о произведениях. Сами произведения не хранятся в YaMDb, вы не можете посмотреть фильм или послушать музыку здесь. Произведения разделены на категории: "Книги", "Фильмы", "Музыка". Список категорий может быть расширен администратором. Произведению может быть присвоен жанр из заранее определенного списка (например, "Сказка", "Рок" или "Артхаус"). Список жанров может быть расширен администратором. Пользователи могут оставлять текстовые отзывы о произведениях и оценивать их от 1 до 10; на основе оценок пользователей формируется средняя оценка работы - рейтинг. Пользователь может оставить только один отзыв на работу.

## Как запустить проект:
1. Клонировать репозиторий:
```git clone git@github.com:Villhard/api_yamdb.git```

2. Перейти в корневую директорию проекта:  
```cd api_yamdb```

3. Cоздать и активировать виртуальное окружение:  
Для macOS/Linux:  
```python3 -m venv venv```  
```source env/bin/activate```  
Для Windows:  
```python -m venv venv```  
```source venv/Scripts/activate```  

4. Обновить пакетный менеджер pip:  
Для macOS/Linux:  
```python3 -m pip install --upgrade pip```  
Для Windows:  
```python -m pip install --upgrade pip```  

5. Установить зависимости из файла requirements.txt:  
```pip install -r requirements.txt```  

6. Создать .env файл и добавить в него переменные:  
Email: ```EMAIL_LOGIN```  
Пароль: ```EMAIL_PASSWORD```

7. Перейти в рабочую папку проекта:  
```cd api_yamdb```  

8. Опция: загрузить тестовые фикстуры:  
```python manage.py load_csv```

9. Выполнить миграции:  
Для macOS/Linux:  
```python3 manage.py migrate```  
Для Windows:  
```python manage.py migrate```

10. Запустить проект:  
Для macOS/Linux:  
```python3 manage.py runserver```  
Для Windows:  
```python manage.py runserver```

## Документация
Пользовательскую документацию можно посмотреть по
[ссылке](http://127.0.0.1:8000/redoc/)


## Авторы проекта
[Рябов Виктор](https://github.com/Villhard)  
[Клоповский Александр](https://github.com/Alexer-s)  
[Дударев Михаил](https://github.com/Palmer656)  
Постановка ТЗ и наполнение проекта: [Yandex-prakticum](yandex-praktikum/api_yatube)


## Примеры запросов на эндпоинты
### Авторизация

- получить код подтверждения:
```POST /api/v1/auth/signup/```
```
{
  "email": "string",
  "username": "string"
}
```

- получить токен:
```POST /api/v1/auth/token/```
```
{
    "username": "string",
    "confirmation_code": "string"
}
```

### Категории

- Получить список всех категорий:
```GET /api/v1/categories/```

- Добавить новую категорию:
```POST /api/v1/categories/```
```
{
  "name": "string",
  "slug": "^-$"
}
```

### Жанры

- Получить список всех жанров:
```GET /api/v1/genres/```

- Добавить новый жанр:
```POST /api/v1/genres/```
```
{
  "name": "string",
  "slug": "^-$"
}
```


### Произведения

- Получить список всех произведений:
```GET /api/v1/titles/```

- Получить данные произведения:
```GET /api/v1/titles/{titles_id}/```

- Добавить новое произведение:
```POST /api/v1/titles/```
```
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```

### Отзывы

- Получить список всех отзывов к произведения:
```GET /api/v1/titles/{title_id}/reviews/```

- Получить данные отзыва:
```GET /api/v1/titles/{title_id}/reviews/{review_id}/```

- Добавить новый отзыв:
```POST /api/v1/titles/{title_id}/reviews/```
```
{
  "text": "string",
  "score": 1
}
```

### Комментарии

- Получить список всех комментариев к отзыву:
```GET /api/v1/titles/{title_id}/reviews/{review_id}/comments/```

- Получить данные комментария:
```GET /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/```

- Добавить новый комментарий:
```POST /api/v1/titles/{title_id}/reviews/{review_id}/comments/```
```
{
  "text": "string"
}
```