from rest_framework.serializers import *
from basket.serializers.other import serializers as goods_serializers
from store.models import Goods


class BasketAddSerializer(Serializer):
    """
    Для добавления товаров в корзину. "override" определяет, нужно ли
    перезаписать количество указанного товара в корзине, или же нужно
    добавить к существующему.
    """
    goods = PrimaryKeyRelatedField(queryset=Goods.objects.all())
    amount = IntegerField(min_value=1)
    override = BooleanField(required=False, default=False)


class BasketItemSerializer(Serializer):
    """
    Сериализатор для отображения данных о товаре в корзине.
    """
    goods = goods_serializers.GoodsBasketSerializer()
    amount = IntegerField()
    price = DecimalField(max_digits=10, decimal_places=2)
    total_price = DecimalField(max_digits=10, decimal_places=2)