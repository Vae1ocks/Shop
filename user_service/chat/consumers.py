from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.db.models import QuerySet, Q

from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.observer import model_observer
from djangochannelsrestframework.observer.generics import ObserverModelInstanceMixin
from djangochannelsrestframework.decorators import action
from djangochannelsrestframework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
)

from rest_framework.utils.serializer_helpers import ReturnDict
from rest_framework import status

from typing import Tuple

from chat.models import Chat, Message
from chat.serializers.chat import serializers
from chat.permissions.websocket.permissions import IsStaff, IsClient


class ChatSupportConsumer(
    ListModelMixin, ObserverModelInstanceMixin, GenericAsyncAPIConsumer
):
    queryset = Chat.objects.filter(support=None)
    serializer_class = serializers.ChatListSerializer

    async def get_permissions(self, action: str, **kwargs):
        if action == "list" or action == "connect":
            # список всех вопросов могут просматривать только сотрудники
            return [IsStaff()]
        # if action == 'retrieve':
        #     instance = self.get_object(**kwargs)
        #     if instance.support is None:
        #         return [IsStaff()]
        # return [IsEmployeeIssue]
        return []


class SupportPersonalChats(
    ListModelMixin, ObserverModelInstanceMixin, GenericAsyncAPIConsumer
):
    permission_classes = [IsStaff]

    def get_queryset(self, **kwargs) -> QuerySet:
        user = self.scope["user"]
        if self.action == "list":
            return Chat.objects.filter(support=user)
        return Chat.objects.filter(support=None)

    # async def get_action_name(self, content, **kwargs):
    #     """
    #     Я не знаю, откуда мне взять action. Автор библиотеки нигде
    #     не делает его self.action, а из content удаляет в этом же методе
    #     get_action_name, далее начинает action гонять по разным методам,
    #     но не делает его атрибутом объекта класса с помощью self.action,
    #     мб в kwargs, но не смотрел.
    #     """
    #     self.action = content.pop("action")
    #     return (self.action, content)
    #
    # def get_serializer_class(self, **kwargs):
    #     if self.action == 'list':
    #         return serializers.ChatListSerializer
    #     return serializers.ChatDetailSerializer
    #
    # @action()
    # def retrieve(self, **kwargs) -> Tuple[ReturnDict, int]:
    #     instance = self.get_object(**kwargs)
    #     serializer = self.get_serializer(instance=instance,
    #                                      action_kwargs=kwargs)
    #     return serializer.data, status.HTTP_200_OK


# class PersonalChats(RetrieveModelMixin,
#                     ListModelMixin,
#                     ObserverModelInstanceMixin,
#                     GenericAsyncAPIConsumer):
#     def get_queryset(self, **kwargs):
#         user = self.scope['user']
#         return Chat.objects.filter(
#             Q(client=user),
#             Q(support=user)
#         )
#
#     def get_serializer_class(self, **kwargs):
#         if self.action == 'list':
#             return serializers.ChatListSerializer
#         return serializers.ChatDetailSerializer
#
#
# class CreateMessageConsumer(CreateModelMixin,
#                             GenericAsyncAPIConsumer):
#     serializer_class = serializers.MessageSerializer


class PersonalChatConsumer(ObserverModelInstanceMixin, GenericAsyncAPIConsumer):
    queryset = Chat.objects.all()
    serializer_class = serializers.ChatDetailSerializer

    @action()
    async def issue_solved(self, pk, **kwargs):
        ...
        # Логика изменения статуса модели Chat на solved=True

    @action()
    async def create_message(self, message, pk, **kwargs):
        chat = await self.get_chat(pk=pk)
        await database_sync_to_async(Message.objects.create)(
            chat=chat, sender=self.scope["user"], text=message
        )

    @action()
    async def subscribe_to_messages_in_chat(self, pk, **kwargs):
        await self.message_activity.subscribe(chat=pk)

    @model_observer(Message)
    async def message_activity(self, message, observer=None, **kwargs):

        await self.send_json(message)

    @message_activity.serializer
    def message_activity(self, instance: Message, action, **kwargs):
        return serializers.MessageSerializer(instance).data

    @database_sync_to_async
    def get_chat(self, pk) -> Chat:
        return Chat.objects.get(pk=pk)
