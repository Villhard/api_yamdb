from django.contrib import admin

from users.models import User
from .models import Category


admin.site.register(Category)
admin.site.register(User)
