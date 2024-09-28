from rest_framework.serializers import *

from django.contrib.auth import get_user_model


class UserInChatSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["first_name", "profile_picture"]
