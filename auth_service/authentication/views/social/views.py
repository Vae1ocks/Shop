"""
Для аутентификации через сторонние сервисы.
"""
from random import random

import requests
import pkce
import string

from rest_framework.generics import GenericAPIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.status import *
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

from django.conf import settings
from django.contrib.auth import get_user_model

from authentication.serializers.social import serializers
from authentication.social_services.google import check_google_token
from authentication.social_services.yandex import check_yandex_token
from authentication.social_services.vk import check_vk_token
from authentication.serializers.social.serializers import TokenSerializer

User = get_user_model()


def create_tokens_for_user(user):
    token = RefreshToken.for_user(user)
    token.payload.update(
        {
            'user_id': user.pk,
        }
    )
    tokens = {
        'refresh': str(token),
        'access': str(token.access_token)
    }
    return tokens


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
            tokens = create_tokens_for_user(user)
            return Response({
                'refresh': tokens['refresh'],
                'access': tokens['access']
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
        tokens = create_tokens_for_user(user)
        return Response({
            'refresh': tokens['refresh'],
            'access': tokens['access']
        }, HTTP_200_OK)

class VKSecurity(GenericAPIView):
    """
    Аутентификация по ВК.
    """
    @extend_schema(
        description='Для аутентификации с использованием ВК. Для передачи данных требуются '
                    'code_verifier и code_challenge. state - случайный набор символов. '
    )
    def get(self, request, *args, **kwargs):
        data = {
            'code_verifier': pkce.generate_code_verifier(43),
            'code_challenge': pkce.get_code_challenge(code_verifier),
            'state': ''.join(random.choice(string.ascii_lowercase) for i in range(15)),
        }

        return Response({'data': data}, status=HTTP_200_OK)


class VkAuth(GenericAPIView):
    serializer_class = TokenSerializer

    @extend_schema(
        description='Для аутентификации с использованием ВК.'
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = check_vk_token(serializer)
        token = create_tokens_for_user(user)
        return Response({
            'refrest': token['refresh'],
            'access': token['access']
        }, status=status.HTTP_200_OK)



