from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field, OpenApiTypes

from ...models import Category, Goods, Comment, PriceHistory, ImageModel


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageModel
        fields = ["image"]


class CommentSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, required=False)

    class Meta:
        model = Comment
        exclude = ["author"]

    def create(self, validated_data):
        images_data = validated_data.pop("images", [])
        request = self.context["request"]
        user_id = request.user.id
        validated_data["author"] = user_id
        comment = super().create(validated_data)
        for image_data in images_data:
            ImageModel.objects.create(
                comment=comment,
                **image_data,
            )
        return comment


class CommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "body", "rating"]


class PriceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceHistory
        exclude = ["goods"]


class GoodsListSerializer(serializers.ModelSerializer):
    available = serializers.SerializerMethodField()

    class Meta:
        model = Goods
        fields = [
            "id",
            "image",
            "title",
            "price",
            "rating",
            "available",
        ]

    @extend_schema_field(OpenApiTypes.BOOL)
    def get_available(self, obj):
        if obj.amount >= 1:
            return True
        return False


class GoodsDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(
        many=True,
        read_only=True,
    )
    price_history = PriceHistorySerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Goods
        exclude = ["slug"]
