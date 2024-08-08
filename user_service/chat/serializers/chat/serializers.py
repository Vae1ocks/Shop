from rest_framework.serializers import *

from chat.models import Chat

class ChatClientListSerializer(ModelSerializer):
    class Meta:
        model = Chat
        exclude = ['client']
