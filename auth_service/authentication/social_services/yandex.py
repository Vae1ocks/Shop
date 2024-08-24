from rest_framework.exceptions import AuthenticationFailed
from rest_framework.status import *

from django.contrib.auth import get_user_model

from authentication.serializers.social.serializers import TokenSerializer

import requests

User = get_user_model()

token_verify_url = 'https://login.yandex.ru/info?'


def check_yandex_token(serializer: TokenSerializer) -> User:
    token = serializer.data['token']

    headers = {
        "Authorization": f"OAuth {token}",
        "Accept": "application/json"
    }
    params = {
        "format": "json"
    }
    response = requests.get(
        token_verify_url, headers=headers, params=params
    )

    if response.status_code != HTTP_200_OK:
        raise AuthenticationFailed(
            'Неверные данные', HTTP_401_UNAUTHORIZED
        )

    data = response.json()
    first_name = data['first_name']
    if not first_name:
        first_name = data['login']

    user, _ = User.objects.get_or_create(
        email=data['email'],
        defaults={
            'first_name': first_name,
            'password': ''
        }
    )
    return user
