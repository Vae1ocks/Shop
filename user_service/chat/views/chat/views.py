from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import get_user_model

from drf_spectacular.utils import extend_schema

from chat.serializers.chat import serializers
from chat.models import Chat


class ChatListView(GenericAPIView):
    serializer_class = serializers.ChatClientListSerializer

    def get(self, request, *args, **kwarg):
        chats = Chat.objects.filter(client_id=request.user.id)
        serializer = serializers.ChatClientListSerializer(chats, many=True)
        return Response(serializer.data, HTTP_200_OK)