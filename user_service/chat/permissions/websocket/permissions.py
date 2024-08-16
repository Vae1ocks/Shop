from typing import Dict, Any

from channels.consumer import AsyncConsumer
from djangochannelsrestframework.permissions import BasePermission
from channels.db import database_sync_to_async

from django.contrib.auth import get_user_model


@database_sync_to_async
def get_user(id):
    return get_user_model().objects.get(id=id)


class IsStaff(BasePermission):
    async def has_permission(self, scope, consumer, action, **kwargs) -> bool:
        user = await get_user(id=scope['user'].id)
        return True if user.is_staff else False


class IsClient(BasePermission):
    async def has_permission(self, scope, consumer, action, **kwargs) -> bool:
        user = await get_user(id=scope['user'].id)
        return True if not user.is_staff else False


# class IsPersonsChat(BasePermission):
#     def has_permission(self, scope, consumer, **kwargs) -> bool:
#         user = get_user(id=scope['user'].id)