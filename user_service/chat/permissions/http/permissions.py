from rest_framework.permissions import BasePermission, IsAuthenticated

from django.contrib.auth import get_user_model


class IsUsersChat(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not IsAuthenticated().has_permission(request, view):
            return False

        user_id = request.user.id
        if obj.client.id == user_id or obj.support.id == user_id:
            return True
        return False
