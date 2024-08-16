from django.contrib.auth import get_user_model
from django.db.models import QuerySet, Q

from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.observer.generics import ObserverModelInstanceMixin
from djangochannelsrestframework.decorators import action
from djangochannelsrestframework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin
)

from rest_framework.utils.serializer_helpers import ReturnDict
from rest_framework import status

from typing import Tuple

from chat.models import Chat, Message
from chat.serializers.chat import serializers
from chat.permissions.websocket.permissions import IsStaff, IsClient


class ChatSupportConsumer(
    ListModelMixin,
    ObserverModelInstanceMixin,
    GenericAsyncAPIConsumer
):
    queryset = Chat.objects.filter(support=None)
    serializer_class = serializers.ChatListSerializer

    async def get_permissions(self, action: str, **kwargs):
        if action == 'list' or action == 'connect':
            # список всех вопросов могут просматривать только сотрудники
            return [IsStaff()]
        # if action == 'retrieve':
        #     instance = self.get_object(**kwargs)
        #     if instance.support is None:
        #         return [IsStaff()]
        # return [IsEmployeeIssue]
        return []


class SupportPersonalChats(
    ListModelMixin,
    ObserverModelInstanceMixin,
    GenericAsyncAPIConsumer
):
    permission_classes = [IsStaff]

    def get_queryset(self, **kwargs) -> QuerySet:
        user = self.scope['user']
        if self.action == 'list':
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

