from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор пользователя.
    """

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'role',
            'bio',
        )

    def validate_username(self, value):
        """
        Проверка что username не 'me'.
        """
        if value == 'me':
            raise ValidationError('Username не может быть "me"')
        return value
