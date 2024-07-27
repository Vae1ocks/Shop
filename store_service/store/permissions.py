from rest_framework.permissions import *
from .models import Goods


class IsGoodsBoughtByUser(BasePermission):
    def has_permission(self, request, view):
        goods_id = request.data.get('goods')
        if not goods_id:
            return False

        try:
            goods = Goods.objects.get(id=goods_id)
        except Goods.DoesNotExist:
            return False

        if request.user.id not in goods.users_bought:
            return False

        return True


class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user.id
