from rest_framework.generics import *
from rest_framework.response import Response
from rest_framework.status import *
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    inline_serializer,
    OpenApiResponse,
    OpenApiTypes,
)

from basket.basket import Basket
from basket.serializers.basket import serializers
from store.models import Goods


class BasketAddGoodsView(GenericAPIView):
    serializer_class = serializers.BasketAddSerializer

    @extend_schema(
        description="Поле override необязательно, по дефолту установлено в False, "
        "определяет, нужно ли количество товара, переданное в тело "
        "запроса перезаписать, или же добавить к существующему. Т.е "
        "если есть товар, которого 5 штук и делает post-запрос для "
        "добавления этого товара в корзину с количеством 9 и "
        "override=True, то количество товара в корзине составит 9, "
        "иначе - 14.",
        responses={
            200: inline_serializer(
                name="Success Response", fields={"detail": serializers.CharField()}
            ),
        },
        examples=[
            OpenApiExample(
                "Пример успешного ответа",
                summary="Пример успешного ответа",
                value={"detail": "Товар добавлен в корзину"},
                response_only=True,
            ),
        ],
    )
    def post(self, request, *args, **kwargs):
        basket = Basket(request)
        serializer = serializers.BasketAddSerializer(data=request.data)
        if serializer.is_valid():
            goods = get_object_or_404(Goods, id=serializer.data["goods"])
            basket.add(
                goods,
                serializer.data["amount"],
                serializer.data["override"],
            )
            return Response(
                {"detail": "Товар добавлен в корзину"},
                HTTP_200_OK,
            )
        return Response(
            serializer.errors,
            HTTP_400_BAD_REQUEST,
        )


class BasketRemoveGoodsView(GenericAPIView):
    @extend_schema(
        description="Для удаления товара из корзины, требуется лишь id товара",
        request=inline_serializer(
            name="Remove Data",
            fields={
                "goods_id": serializers.PrimaryKeyRelatedField(
                    queryset=Goods.objects.all()
                )
            },
        ),
        responses={
            200: inline_serializer(
                name="Success Response", fields={"detail": serializers.CharField()}
            ),
            400: inline_serializer(
                name="Error 400 Response", fields={"detail": serializers.CharField()}
            ),
        },
        examples=[
            OpenApiExample(
                "Пример успешного ответа",
                summary="Пример успешного ответа",
                value={"detail": "Товар удалён из корзины"},
                response_only=True,
            ),
            OpenApiExample(
                "Пример ответа в случае 400-ой ошибки",
                summary="Пример ответа в случае 400-ой ошибки",
                value={"detail": "Товар удалён из корзины"},
                response_only=True,
            ),
        ],
    )
    def post(self, request):
        basket = Basket(request)
        if "goods_id" in request.data:
            goods = get_object_or_404(Goods, id=request.data["goods_id"])
            basket.remove(goods)
            return Response(
                {"detail": "Товар удалён из корзины"},
                HTTP_204_NO_CONTENT,
            )
        return Response(
            {"detail": "Необходимо предоставить товар"},
            HTTP_400_BAD_REQUEST,
        )


class BasketDetailView(GenericAPIView):
    serializer_class = serializers.BasketItemSerializer

    @extend_schema(
        description="Для получения детальной информации о корзине,"
        "возвращает список сериализованных объектов"
    )
    def get(self, request):
        basket = Basket(request)
        basket_items = basket.get_basket_items()
        serializer = serializers.BasketItemSerializer(basket_items, many=True)
        return Response(serializer.data, HTTP_200_OK)
