from django.contrib import admin

from .models import Category, Genre, Title, Review, Comment


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    list_display_links = ('name',)


class GenreInline(admin.TabularInline):
    model = Title.genre.through
    verbose_name = 'Жанр произведения'
    verbose_name_plural = 'Жанры'
    extra = 0


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    list_display_links = ('name',)


class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'description', 'category')
    search_fields = ('name', 'description', 'year')
    list_filter = ('category', 'genre', 'year')
    list_display_links = ('name',)
    filter_horizontal = ('genre',)
    inlines = (GenreInline,)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'text', 'score', 'pub_date')
    search_fields = ('text',)
    list_filter = ('score',)
    list_display_links = ('title',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('review', 'author', 'text', 'pub_date')
    search_fields = ('text',)
    list_display_links = ('review',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.empty_value_display = '-пусто-'
