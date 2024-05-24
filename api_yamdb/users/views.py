from django.core.mail import EmailMessage
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from api_yamdb.settings import EMAIL_HOST_USER
from .serializers import UserSerializer
from .models import ConfirmationCode
from .utils import generate_code


@api_view(['POST'])
def signup(request):
    """
    Регистрация пользователя.
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()

        code = generate_code()
        confirmation_code = ConfirmationCode(
            user=user,
            code=code, 
        )
        confirmation_code.save()

        email = EmailMessage(
            'Код для подтверждения',
            f'{user.username}, Ваш код для входа\n{confirmation_code.code}',
            EMAIL_HOST_USER,
            [user.email],
        )
        email.send()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
