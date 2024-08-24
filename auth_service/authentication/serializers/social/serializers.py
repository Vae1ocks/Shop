from rest_framework.serializers import *


class GoogleAuthSerializer(Serializer):
    token = CharField()
    email = EmailField()


class TokenSerializer(Serializer):
    token = CharField()


class VkAuthSerializer(Serializer):
    email = EmailField(write_only=True, required=True)