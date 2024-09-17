from rest_framework import serializers

from favorites.models import Favorite
from store.models import Goods
from store.serializers.store.serializers import GoodsListSerializer


class FavoriteSerializer(serializers.ModelSerializer):
    goods = GoodsListSerializer(many=True, read_only=True)
    goods_id = serializers.PrimaryKeyRelatedField(
        queryset=Goods.objects.all(), source='goods', write_only=True
    )

    class Meta:
        model = Favorite
        fields = ['goods_id', 'goods']

    def validate_goods_id(self, value):
        user_id = self.context['request'].user.id
        if Favorite.objects.filter(
            user_id=user_id, goods_id=value
        ).exists():
            raise serializers.ValidationError(
                'Нарушение уникальности: данная модель уже существует.'
            )
        return value

    def create(self, validated_data):
        user_id = self.context['request'].user.id
        validated_data['user_id'] = user_id
        return super().create(validated_data)
