from rest_framework.generics import *
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, OpenApiExample

from user.serializers.another.serializers import *


class CategoriesBoughByUserView(RetrieveAPIView):
    """
    View для межсервисного взаимодействия, используется в store_service в GoodsListView
    """
    serializer_class = CategoriesBoughtByUserSerializer
    queryset = get_user_model().objects.all()

    @extend_schema(description='Для межсервисного бэкенд взаимодействия, '
                               'не для фронтенд части.')
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class UserRepresentationalView(RetrieveAPIView):
    """
    View для межсервисного взаимодействия, используется в
    store_service в CommentCreateView
    """
    serializer_class = UserRepresentationalInfo
    queryset = get_user_model().objects.all()

    @extend_schema(description='Для межсервисного бэкенд взаимодействия, '
                               'не для фронтенд части.')
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class AddPriceExpectation(GenericAPIView):
    serializer_class = PriceExpectationSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description='Для добавления товара в ожидаемые при указанной цене'
    )
    def post(self, request, *args, **kwargs):
        serializer = PriceExpectationSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            user = get_user_model().objects.get(id=request.user.id)
            user.expected_prices[data['goods']] = {
                'title': data['title'],
                'expected_price': data['expected_price']
            }
            user.save()
            return Response({'detail': 'Товар добавлен в ожидаемые'}, HTTP_200_OK)
        return Response(serializer.errors, HTTP_400_BAD_REQUEST)


class RemovePriceExpectation(GenericAPIView):
    serializer_class = PriceExpectationSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description='Для удаления товара из ожидаемых'
    )
    def post(self, request, *args, **kwargs):
        serializer = PriceExpectationSerializer(data=request.data)
        if serializer.is_valid():
            goods = serializer.data['goods']
            expected_price = serializer.data['expected_price']
            user = get_user_model().objects.get(id=request.user.id)
            if goods in user.expected_prices:
                user.expected_prices.pop(goods)
                user.save()
                return Response({'detail': 'Товар удалён из ожидаемых'},
                                HTTP_200_OK)
            '''
            можно и 404-ый код рассмотреть, но 200 выбрал т.к сама апишка корректно
            отработала
            '''
            return Response({'detail': 'Товар отсутствует в ожидаемых'},
                            status=HTTP_200_OK)

        return Response(serializer.errors, HTTP_400_BAD_REQUEST)


class DetailPriceExpectation(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PriceExpectationSerializer
    '''
    этот сериализатор не используется, просто иначе drf_spectacular отказывается
    отображать описанный мною в @extend_schema пример
    '''

    @extend_schema(
        description='Для получения всех ожидаемых товаров, возвращает единый '
                    'json объект, где ключом является id товара',
        examples=[
            OpenApiExample(
                'Пример ответа',
                summary='Пример ответа',
                value={
                    '3': {'title': 'Goods Title1', 'expected_price': 100.5},
                    '25': {'title': 'Goods Title2', 'expected_price': 550},
                    '19': {'title': 'Goods Title3', 'expected_price': 105},
                    '5': {'title': 'Goods Title4', 'expected_price': 120},
                    '44': {'title': 'Goods Title5', 'expected_price': 10000}
                },
                response_only=True

            )
        ]
    )
    def get(self, request, *args, **kwargs):
        user = get_user_model().objects.get(id=request.user.id)
        expected_prices = user.expected_prices
        return Response({'expected_prices': expected_prices}, HTTP_200_OK)