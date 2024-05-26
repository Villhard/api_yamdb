from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.decorators import api_view, action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.filters import SearchFilter

from users.models import ConfirmationCode, User
from users.serializers import UserSerializer, UserSignupSerializer, ObtainTokenSerializer
from users.utils import send_mail
from users.permissions import IsAdmin


@api_view(['POST'])
def signup(request):
    """
    Регистрация пользователя.
    """
    serializer = UserSignupSerializer(data=request.data)
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


@api_view(['POST'])
def token(request):
    """
    Получение токена.
    """
    serializer = ObtainTokenSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data.get('username')
        user = User.objects.get(username=username)
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all().order_by('id')
    lookup_field = 'username'
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    filter_backends = [SearchFilter]
    search_fields = ['username']
    http_method_names = ['get', 'post', 'delete', 'patch']

    @action(detail=False, methods=['get', 'patch'], permission_classes=[IsAuthenticated])
    def me(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['role'] = request.user.role
        serializer.save()
        return Response(serializer.data)
