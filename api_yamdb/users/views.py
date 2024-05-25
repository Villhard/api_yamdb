from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import UserSerializer
from .models import ConfirmationCode, User
from .utils import send_mail


@api_view(['POST'])
def signup(request):
    """
    Регистрация пользователя.
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')

        user, _ = User.objects.get_or_create(
            username=username,
            email=email,
        )
        code = get_random_string(length=6, allowed_chars='1234567890')
        ConfirmationCode.objects.update_or_create(
            user=user,
            defaults={'code': code},
        )

        send_mail(user, code)

        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
