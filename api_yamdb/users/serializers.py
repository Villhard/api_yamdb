from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор пользователя.
    """
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'email',
            'username',
        )

    def validate(self, data):
        """
        Проверка на полное совпадение username и email с существующим пользователем.
        """
        username = data.get('username')
        email = data.get('email')

        user_with_same_username_and_email = User.objects.filter(
            username=username,
            email=email
        ).exists()
        user_with_same_username = User.objects.filter(
            username=username
        ).exists()
        user_with_same_email = User.objects.filter(
            email=email
        ).exists()

        if user_with_same_username_and_email:
            return data
        elif user_with_same_username and user_with_same_email:
            raise ValidationError({
            'username': 'Пользователь с таким username уже существует',
            'email': 'Пользователь с таким email уже существует',
            })
        elif user_with_same_username:
            raise ValidationError({'username': 'Пользователь с таким username уже существует'})
        elif user_with_same_email:
            raise ValidationError({'email': 'Пользователь с таким email уже существует'})
        return data
