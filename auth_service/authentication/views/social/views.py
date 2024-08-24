"""
Для аутентификации через сторонние сервисы
"""
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

from authentication.serializers.social import serializers
from authentication.social_services.google import check_google_token
from authentication.serializers.social.serializers import TokenSerializer
from authentication.models import User


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


class VKSecurity(GenericAPIView):

    def get(self, request, *args, **kwargs):
        data = {
            'code_verifier': pkce.generate_code_verifier(43),
            'code_challenge': pkce.get_code_challenge(code_verifier),
            'state': ''.join(rangom.choice(string.ascii_lowercase) for i in range(15)),
        }
        print(data['state'])

        return Response({'data': data}, status=HTTP_200_OK)


"""
token = sdafsasdfa
url = https://id.vk.com/oauth2/public_info/?access_token={token}
response = requests.post(url)
user_email = response.json()['email']

user = User.objects.get_or_create(email=user_email)
password = ''
authetication(user)
return Responce
"""

class VkAuth(GenericAPIView):
    serializer_class = VkAuthSerializer

    def post(self, request, *args, **kwargs):
        id_token = request.data['token']
        client_id = settings.SOCIAL_AUTH_VK_KEY
        url = f'https://id.vk.com/oauth2/public_info?client_id={client_id}&id_token={id_token}'
        response = requests.post(url)
        user_email = response.json()['email']
        user = User.objects.get_or_create(email=user_email, defults={'password': '', 'is_verified': True})
        user_password = user.password
        user_login = authenticate(email=user_email, password=user_password)
        token = RefreshToken.for_user(user)
        token.payload.update({
            'user_id': user.pk,
        })
        return Response({
            'refresh': str(token),
            'access': str(token.access_token)
        }, status=status.HTTP_200_OK)

