from rest_framework import serializers
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

    def create(self, validated_data):
        if validated_data['username'].lower() == 'me':
            raise serializers.ValidationError(
                {
                    'username': [
                        'Нельзя использовать имя пользователя "me"'
                    ]
                }
            )
        return User.objects.create_user(**validated_data)
