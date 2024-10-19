from rest_framework.serializers import *
from store.models import Goods


class GoodsBasketSerializer(ModelSerializer):
    class Meta:
        model = Goods
        fields = ["id", "title"]
