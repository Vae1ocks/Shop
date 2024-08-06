"""API для authentication"""

import datetime
import random

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status

from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.authentication import authenticate
from django.contrib.auth.hashers import check_password, make_password
from django.utils import timezone

from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
from celery import current_app

from authentication.serializers.auth.serializers import *
from authentication.tasks import *


User = get_user_model()


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
            short_code = str(random.randrange(100000, 999999))
            full_code = make_password(short_code)
            request.session.set_expiry(300)
            request.session['reg'] = {
                'email': serializer.validated_data.get('email'),
                'first_name': serializer.validated_data.get('first_name'),
                'full_code': full_code,
                'expire_at': str(datetime.datetime.now() + timezone.timedelta(minutes=5))
            }

            send_mail_code_task.delay(
                user_email=serializer.validated_data.get('email'),
                first_name=serializer.validated_data.get('first_name'),
                code=short_code
            )
            return Response({'detail': f'Письмо отправлено. Код: {short_code}'},
                            status=status.HTTP_200_OK)


class ConfirmRegistration(generics.GenericAPIView):
    serializer_class = SendCodeSerializer
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        description='Заполняется обязательное поле с кодом, который был отправлен '
                    'на email пользователю. Если код совпадает с кодом в сессии '
                    'то происходит создание пользователя.'
    )
    def post(self, request, *args, **kwargs):
        short_code = request.data.get('short_code')
        full_code = request.session['reg'].get('full_code')
        if check_password(short_code, full_code):
            if request.session['reg'].get('expire_at') > str(datetime.datetime.now()):
                return Response({'detail': f'Код введен верно'}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Время действия кода истекло.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Код не совпадает'}, status=status.HTTP_400_BAD_REQUEST)


class SetNewPassword(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = SetNewPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        session_reg = request.session['reg']
        user = User.objects.create_user(
            email=session_reg['email'],
            first_name=session_reg['first_name'],
            password=serializer.validated_data['password'],
            is_verified=True,
        )
        user.save()
        # Создать task с отправкой в user_service данные пользователя.
        current_app.send_task(
            'send_data_user_create_user',
            kwargs={
                'email': request.session['reg'].get('email'),
                'first_name': request.session['reg'].get('first_name'),
                'password': serializer.validated_data['password']
            },
            queue='user_system_queue'
        )
        return Response({'detail': f'Пользователь {user.email} создан.'}, status=status.HTTP_200_OK)


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
            return Response({'detail': 'Неверные авторизационные данные'},
                            401)
        token = RefreshToken.for_user(user)
        token.payload.update({
            'user_id': user.pk,
        })
        return Response({
            'refresh': str(token),
            'access': str(token.access_token)
        }, status=status.HTTP_200_OK)


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
        return Response({'detail': 'Выход выполнен.'}, status=status.HTTP_200_OK)


class GenerateAccessToken(generics.GenericAPIView):
    serializer_class = RefreshSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        description='При отправке refresh токена генерируется access токен для входа.'
    )
    def post(self, request, *args, **kwargs):
        refresh = request.data.get('refresh')
        token = RefreshToken(refresh)
        return Response({'access': str(token.access_token)}, status=status.HTTP_200_OK)


class ResetPassword(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            short_code = str(random.randrange(100000, 999999))
            full_code = make_password(short_code)
            request.session['reset'] = {
                'email': email,
                'full_code': full_code
            }

            send_mail_code_task.delay(
                user_email=user.email,
                first_name=user.first_name,
                code=short_code)
            return Response({'detail': f'Письмо отправлено. Код: {short_code}'}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'detail': f'Такого пользователя не существует.'},status=status.HTTP_400_BAD_REQUEST)


class ConfirmResetPassword(generics.GenericAPIView):
    serializer_class = SendCodeSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        short_code = request.data.get('short_code')
        email = request.session['reset'].get('email')
        full_code = request.session['reset'].get('full_code')
        if check_password(short_code, full_code):
            return Response({'detail': 'Код введен верно.'}, status=status.HTTP_200_OK)
        return Response({'detail': 'Код введен не верно.'}, status=status.HTTP_400_BAD_REQUEST)

