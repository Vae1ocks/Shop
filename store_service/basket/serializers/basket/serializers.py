from rest_framework.serializers import *
from basket.serializers.other import serializers as goods_serializers
from store.models import Goods


class BasketAddSerializer(Serializer):
    goods = PrimaryKeyRelatedField(queryset=Goods.objects.all())
    amount = IntegerField(min_value=1)
    override = BooleanField(required=False, default=False)


class BasketItemSerializer(Serializer):
    goods = goods_serializers.GoodsBasketSerializer()
    amount = IntegerField()
    price = DecimalField(max_digits=10, decimal_places=2)
    total_price = DecimalField(max_digits=10, decimal_places=2)