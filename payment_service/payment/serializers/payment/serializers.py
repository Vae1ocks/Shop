from rest_framework.serializers import *
from ..other.serializers import GoodsInBasketSerializer


class BasketItemDataSerializer(Serializer):
    goods = GoodsInBasketSerializer()
    amount = IntegerField()
    price = DecimalField(max_digits=10, decimal_places=2)