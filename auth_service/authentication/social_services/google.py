from rest_framework.exceptions import AuthenticationFailed
from rest_framework.status import *
from django.contrib.auth import get_user_model
from django.conf import settings

from ..serializers.social.serializers import GoogleAuthSerializer
from google.oauth2 import id_token
from google.auth.transport import requests

User = get_user_model()


def check_google_token(google_serializer: GoogleAuthSerializer) -> User:
    """
    Функция валидации токена Google и проверки, существует ли пользователь с email
    или же необходимо создать пользователя. В случае отсутствия пользователя с
    указанным email, создаём с использованием get_or_create. Не создаю пользователя
    с использованием create_user, т.к. мы не получаем пароль, так что создаю
    пользователя с пустым паролем чтобы не допустить хеширование пустого пароля, чтобы
    в любом случае не было возможности авторизоваться за данного пользователя.
    """
    google_data = google_serializer.data
    try:
        id_token.verify_oauth2_token(google_data['token'], requests.Request(),
                                     settings.GOOGLE_CLIENT_ID)
    except ValueError:
        raise AuthenticationFailed('Неверный Google токен', HTTP_403_FORBIDDEN)

    email = google_data['email']
    user, _ = User.objects.get_or_create(
        email,
        defaults={
            'password': '',
        }
    )
    return user
