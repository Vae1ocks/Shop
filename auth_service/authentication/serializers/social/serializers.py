from rest_framework.serializers import *


class GoogleAuthSerializer(Serializer):
    token = CharField()
    email = EmailField()


class TokenSerializer(Serializer):
    token = CharField()