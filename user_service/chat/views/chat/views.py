from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema

from chat.serializers.chat import serializers
from chat.models import Chat
from chat.permissions.http.permissions import IsUsersChat


class ChatListView(GenericAPIView):
    serializer_class = serializers.ChatClientListSerializer

    def get(self, request, *args, **kwarg):
        chats = Chat.objects.filter(client_id=request.user.id)
        serializer = serializers.ChatClientListSerializer(chats, many=True)
        return Response(serializer.data, HTTP_200_OK)


class ChatCreateView(GenericAPIView):
    serializer_class = serializers.ChatCreateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = serializers.ChatCreateSerializer(request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)


class ChatRetrieveView(GenericAPIView):
    permission_classes = [IsUsersChat]
    serializer_class = serializers.ChatDetailSerializer

    def get(self, request, *args, **kwargs):
        chat = self.get_object()
        user = get_user_model().objects.get(id=request.user.id)
        if user.is_staff and chat.support is None:
            chat.support = user
            chat.save()
        serializer = serializers.ChatDetailSerializer(chat)
        return Response(serializer.data, HTTP_200_OK)
