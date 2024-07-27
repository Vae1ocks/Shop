import random
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import permissions
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.authentication import authenticate
from django.contrib.auth.hashers import check_password, make_password
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema

from authentication.models import User
from authentication.serializers.auth.serializers import *


# TODO: Донастроить отправку Email в настройках
class Registration(generics.GenericAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        description='Заполняются все поля данными. Происходит проверка паролей. '
                    'Если поля заполнены правильно, данные записываются в сессию и '
                    'отправляется письмо на почту для подтверждения регистрации.'
    )
    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            full_code = make_password(str(random.randrange(100000, 999999)).encode('utf-8'))
            if full_code[-7] == '/':
                full_code[-7] = 'a'
            request.session['reg'] = {
                'email': serializer.validated_data.get('email'),
                'first_name': serializer.validated_data.get('first_name'),
                'code': full_code
            }
            short_code = full_code[len(full_code) - 7:]
            subject = f'Регистрация'
            message = (f'{serializer.validated_data['first_name']}, для подтверждения регистрации перейдите по ссылке '
                       f'http://127.0.0.1:8000/{short_code}')
            send_mail(subject, message, settings.EMAIL_HOST_USER, [serializer.data['email']])
            return Response({'detail': f'Письмо отправлено. Код: {short_code}'})


class ConfirmRegistration(generics.GenericAPIView):
    serializer_class = ConfirmRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        description='Заполняется обязательное поле с кодом, который был отправлен '
                    'на email пользователю. Если код совпадает с кодом в сессии '
                    'то происходит создание пользователя.'
    )
    def post(self, request, *args, **kwargs):
        short_code = kwargs['short_code']
        full_code = request.session['reg'].get('code')
        serializer = ConfirmRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if short_code == full_code[len(full_code) - 7:]:
            user = User.objects.create_user(
                email=request.session['reg'].get('email'),
                first_name=request.session['reg'].get('first_name'),
                password=serializer.validated_data['password'],
                is_verified=True,
            )
            del request.session['reg']
            return Response({'detail': f'Пользователь {user.email} создан'})
        return Response({'detail': 'Код не совпадает'})


class Login(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        description='Если поля заполнены верно и пользователь существует '
                    '- Выдается 2 токена. Access и Refresh. Вход осуществляется по '
                    'access токену.'
    )
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if not user:
            return Response({'detail': 'Неверный логин'})
        token = RefreshToken.for_user(user)
        token.payload.update({
            'user_id': user.pk,
        })
        return Response({
            'refresh': str(token),
            'access': str(token.access_token)
        })


class Logout(generics.GenericAPIView):
    serializer_class = RefreshSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        description='Если токен действителен, то он заносится в черный список. '
                    'Токен становится недействительным.'
    )
    def post(self, request, *args, **kwargs):
        refresh = request.data.get('refresh')
        token = RefreshToken(refresh)
        token.blacklist()
        return Response({'detail': 'Выход выполнен.'})


class GenerateAccessToken(generics.GenericAPIView):
    serializer_class = RefreshSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        description='При отправке refresh токена генерируется access токен для входа.'
    )
    def post(self, request, *args, **kwargs):
        refresh = request.data.get('refresh')
        token = RefreshToken(refresh)
        return Response({'access': str(token.access_token)})
