from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    roles = ('user', 'moderator', 'admin')

    password = models.CharField(max_length=128, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    role = models.CharField(
        max_length=50, blank=True, null=True, choices=roles, default='user'
    )
