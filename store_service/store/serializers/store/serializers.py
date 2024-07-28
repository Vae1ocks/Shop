from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field, OpenApiTypes

from ...models import Category, Goods, Comment, PriceHistory


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        exclude = ['author']

    def create(self, validated_data):
        request = self.context['request']
        user_id = request.user.id
        validated_data['author'] = user_id
        return super().create(validated_data)


class CommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'body', 'rating']


class PriceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceHistory
        exclude = ['goods']


class GoodsListSerializer(serializers.ModelSerializer):
    available = serializers.SerializerMethodField()

    class Meta:
        model = Goods
        fields = ['id', 'image', 'title', 'price', 'rating', 'available']

    @extend_schema_field(OpenApiTypes.BOOL)
    def get_available(self, obj):
        if obj.amount >= 1:
            return True
        return False


class GoodsDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    price_history = PriceHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Goods
        exclude = ['slug']
