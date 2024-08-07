from rest_framework.serializers import *
from django.contrib.auth import get_user_model


class CategoriesBoughtByUserSerializer(ModelSerializer):
    """
    Для сериализации категорий, товаров которые пользователь купил.
    """
    class Meta:
        model = get_user_model()
        fields = ['categories_bought']


class UserRepresentationalInfo(ModelSerializer):
    """
    Для сериализации информации о пользователе.
    """
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'profile_picture']


class PriceExpectationSerializer(Serializer):
    """
    Для сериализации ожидаемой цены на товар.
    """
    goods = IntegerField()
    title = CharField()
    expected_price = DecimalField(max_digits=10, decimal_places=2)
