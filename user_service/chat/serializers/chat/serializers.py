from rest_framework.serializers import *

from django.contrib.auth import get_user_model

from chat.models import Chat, Message
from chat.serializers.other.serializers import UserInChatSerializer


class ChatClientListSerializer(ModelSerializer):
    class Meta:
        model = Chat
        exclude = ['client']


class ChatListSerializer(ModelSerializer):
    client = UserInChatSerializer()

    class Meta:
        model = Chat
        exclude = ['support']


class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class ChatCreateSerializer(ModelSerializer):
    """
    Для создания нового чата. Использоваться будет пользователями, когда
    они хотят задать вопрос. При этом нужно указать название проблемы -
    атрибут Chat.issue и более подробную информацию о ней - message.
    Т.е у любого чата минимум 1 связанный объект модели Message.
    """
    message = MessageSerializer(write_only=True)

    class Meta:
        model = Chat
        fields = ['issue', 'message']

    def create(self, validated_data):
        user_id = self.context['request'].user.id
        user = get_user_model().objects.get(id=user_id)
        message_data = validated_data.pop('message')
        chat = Chat.objects.create(client=user, **validated_data)
        Message.objects.create(**message_data, chat=chat)
        return chat


class ChatDetailSerializer(ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    user = SerializerMethodField()

    class Meta:
        model = Chat
        exclude = ['client', 'support']

    def get_user(self, obj):
        """
        Вместо сериализации сразу и клиента, и сапорта, определяем, кем
        является текущий пользователь, и в зависимости от этого сериализуем
        нужного пользователя.
        """
        user = self.context['scope']['user']
        if obj.support != user:
            return UserInChatSerializer(obj.support).data
        return UserInChatSerializer(obj.client).data
