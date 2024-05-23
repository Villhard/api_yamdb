from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import UserSerializer


@api_view(['POST'])
def signup(request):
    """
    Регистрация пользователя.

    Параметры запроса:
    - email (email)
    - username (^[\w.@+-]+\Z)
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        send_mail(
            'Регистрация на YamDB',
            'Вы успешно зарегистрировались на YamDB!',
            'monti.python@yandex.ru',
            [user.email],
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
