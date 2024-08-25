import requests

from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework import status



User = get_user_model()


def check_vk_token(serializer):
    id_token = serializer.data['token']
    client_id = settings.SOCIAL_AUTH_VK_KEY
    url = f'https://id.vk.com/oauth2/public_info?client_id={client_id}&id_token={id_token}'
    response = requests.post(url)
    data = response.json()

    user_email = data['email']
    user_photo = data['avatar']
    user_first_name = data['first_name']
    user_last_name = data['last_name']
    user = User.objects.get_or_create(
        email=user_email,
        defaults={
            'password': '',
            'is_verified': True,
        },
        first_name=user_first_name,
        last_name=user_last_name,

    )

    return user
