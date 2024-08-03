from rest_framework.exceptions import AuthenticationFailed
from rest_framework.status import *
from django.contrib.auth import get_user_model
from django.conf import settings

from ..serializers.social.serializers import GoogleAuthSerializer
from google.oauth2 import id_token
from google.auth.transport import requests


def check_google_token(google_serializer: GoogleAuthSerializer):
    google_data = google_serializer.data
    try:
        id_token.verify_oauth2_token(google_data['token'], requests.Request(),
                                     settings.GOOGLE_CLIENT_ID)
    except ValueError:
        raise AuthenticationFailed('Неверный Google токен', HTTP_403_FORBIDDEN)

    email = google_data['email']
    user, _ = get_user_model().objects.get_or_create(email,
                                                     defaults={
                                                         'password': '',
                                                     })
    '''
    Использую метод get_or_create(), который в случае отсутствия модели использует create(),
    не смотря на то, что для создания user существует метод create_user().
    В данном случае делаю так в связи с тем, что от сервиса, используемого
    для соц.аутентификации, мы не получаем пароль, в связи с этим устанавливаем его пустым.
    Далее создаём модель пользователя с использованием create(), а не create_user() чтобы
    не допустить хеширование этого пароля т.к если пустой пароль будет хеширован и где-то
    в бэкенде будет возможность пользователям вводить пустой пароль, то они смогут
    авторизовываться с использованием пустого пароля, что допускать нельзя. 
    '''
    return user