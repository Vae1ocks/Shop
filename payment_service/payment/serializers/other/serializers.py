from rest_framework.serializers import *

from payment.models import Order, OrderItem


class GoodsInBasketSerializer(Serializer):
    goods_id = IntegerField()
    goods_title = CharField()
    amount = IntegerField(default=1)
    price = DecimalField(max_digits=10, decimal_places=2)


class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["goods_id", "goods_title", "amount", "price"]


class OrderListSerializer(ModelSerializer):
    user_id = IntegerField(source="user")
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["id", "user_id", "status", "created", "items"]


class OrderCreateSerializer(ModelSerializer):
    goods = OrderItemSerializer(many=True)
    user_id = IntegerField(source="user.id")

    class Meta:
        model = Order
        fields = ["user_id", "goods"]
