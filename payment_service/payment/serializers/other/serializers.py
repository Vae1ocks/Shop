from rest_framework.serializers import *


class GoodsInBasketSerializer(Serializer):
    goods_id = IntegerField()
    goods_title = CharField()