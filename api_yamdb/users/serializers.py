from re import fullmatch

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор пользователя.
    """

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class UserSignupSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регистрации пользователя.
    """

    username = serializers.CharField(
        max_length=150,
        required=True,
    )
    email = serializers.EmailField(max_length=254, required=True)

    class Meta:
        model = User
        fields = (
            'email',
            'username',
        )

    def validate_username(self, value):
        if value == 'me':
            raise ValidationError('Нельзя использовать это имя')

        if not fullmatch(r'^[\w.@+-]+\Z', value):
            raise ValidationError('Недопустимые символы в имени')

        return value

    def validate(self, data):
        """
        Проверка на полное совпадение username и email
        """
        username = data.get('username')
        email = data.get('email')

        user_with_same_username_and_email = User.objects.filter(
            username=username, email=email
        ).exists()
        user_with_same_username = User.objects.filter(
            username=username
        ).exists()
        user_with_same_email = User.objects.filter(email=email).exists()

        if user_with_same_username_and_email:
            return data
        elif user_with_same_username and user_with_same_email:
            raise ValidationError(
                {
                    'username': 'Пользователь с таким username уже существует',
                    'email': 'Пользователь с таким email уже существует',
                }
            )
        elif user_with_same_username:
            raise ValidationError(
                {'username': 'Пользователь с таким username уже существует'}
            )
        elif user_with_same_email:
            raise ValidationError(
                {'email': 'Пользователь с таким email уже существует'}
            )
        return data


class ObtainTokenSerializer(serializers.Serializer):
    """
    Сериализатор для получения токена.
    """

    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):
        """
        Проверка на существование пользователя с таким username
        и на совпадение кода подтверждения
        """
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')

        user = get_object_or_404(User, username=username)

        if not user.check_confirmation_code(confirmation_code):
            raise ValidationError(
                {'confirmation_code': 'Неверный код подтверждения'}
            )

        return data
