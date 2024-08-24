"""
Для аутентификации через сторонние сервисы.
"""
from rest_framework.generics import GenericAPIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.status import *
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.serializers.social import serializers
from authentication.social_services.google import check_google_token
from authentication.social_services.yandex import check_yandex_token
from authentication.serializers.social.serializers import TokenSerializer


class GoogleAuth(GenericAPIView):
    """
    Для аутентификации по гуглу.
    """
    serializer_class = serializers.GoogleAuthSerializer

    @extend_schema(
        description='Для аутентификации по гуглу'
    )
    def post(self, request, *args, **kwargs):
        """
        Получаем с фронтенда email и токен, передаем данные в check_google_token,
        в случае успеха возвращаем access и refresh токены.
        """
        serializer = serializers.GoogleAuthSerializer(data=request.data)
        if serializer.is_valid():
            user = check_google_token(serializer)
            token = RefreshToken.for_user(user)
            token.payload.update(
                {
                    'user_id': user.pk,
                }
            )
            return Response({
                'refresh': str(token),
                'access': str(token.access_token)
            }, HTTP_200_OK)
        return AuthenticationFailed(
            'Некорректные данные', HTTP_403_FORBIDDEN
        )


class YandexAuth(GenericAPIView):
    """
    Аутентификация с использованием Яндекс.
    """
    serializer_class = serializers.TokenSerializer

    @extend_schema(
        description='Для аутентификации с использованием Яндекс.'
    )
    def post(self, request, *args, **kwargs):
        serializer = serializers.TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = check_yandex_token(serializer)
        token = RefreshToken.for_user(user)
        token.payload.update(
            {
                'user_id': user.pk,
            }
        )
        return Response({
            'refresh': str(token),
            'access': str(token.access_token)
        }, HTTP_200_OK)
