"""
Вьюшки для базового взаимодействия с товарами и с ними связанными:
просмотр списка товаров, категорий, детальная инфа о товарах,
создание/редактирование/удаление комментариев
"""

import requests
from django.core.cache import cache
from drf_spectacular.utils import extend_schema, OpenApiParameter, \
    OpenApiResponse, inline_serializer, OpenApiExample
from rest_framework import mixins
from rest_framework import status
from rest_framework.generics import *
from rest_framework.response import Response

from store import permissions
from store.serializers.store.serializers import *


class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GoodsListView(GenericAPIView):
    def get_recommended_goods(self, queryset):
        """
        Для создания списка рекомендуемых персонально пользователю товаров на
        основе его покупок: делаем запрос к сервису store_service и
        получаем список категорий, кешируем ответ со стороны store_service на 3 часа.
        """
        if self.request.user.is_authenticated:
            base_uri = self.request.build_absolute_uri('/')
            relative_url = f'users/{self.request.user.id}/purchase-history'
            url = f'{base_uri}{relative_url}'
            cache_key = f'user.{self.request.user.id}.purchase-history'
            categories_bought = cache.get(cache_key)

            if categories_bought is None:
                response = requests.get(url)
                if response.status_code == status.HTTP_200_OK:
                    categories_bought = response.json()
                    cache.set(cache_key, categories_bought, timeout=60*60*3)
                else:
                    categories_bought = []
                    # в данном случае мб можно тоже закешировать, только на более
                    # короткий промежуток времени, около 10 минут

            if categories_bought:
                sorted_categories_bought = sorted(
                    categories_bought.items(),
                    key=lambda category: category[1],
                    reverse=True
                )
                sorted_categories_bought = [
                    category for category, count in sorted_categories_bought
                ]
                recommended_goods_list = []
                for category in sorted_categories_bought:
                    # Предлагаем пользователю сначала персональные предложения для его, ограниченный
                    # суммарным количеством до 25, и чтобы обеспечить, что эти товары будут из разных
                    # категорий, для 1 категории ограничиваем количество товаров до 2.
                    # В результате если мы имеем 9 категорий и 1000 товаров этих категорий,
                    # всего в рекомендации попадёт 18 товаров.
                    category_goods = queryset.filter(
                        category__title=category
                    ).order_by('-times_bought')[:2]
                    recommended_goods_list.extend(category_goods)
                    if len(recommended_goods_list) >= 25:
                        break
                return recommended_goods_list
        return []

    @extend_schema(
        parameters=[
            OpenApiParameter(name='title', description='Параметр для фильтрации по названию товаров',
                             required=False, type=OpenApiTypes.STR),
            OpenApiParameter(name='price', description='Фильтрация по цене доступна '
                                                       'в случае наличия параметра title или category в url. '
                                                       'Формат: "min;max"',
                             required=False, type=OpenApiTypes.STR)
        ],
        responses={
            200: OpenApiResponse(
                response=inline_serializer(
                    name='GoodsListResponse',
                    fields={
                        'recommended_goods': GoodsListSerializer(many=True),
                        'other_goods': GoodsListSerializer(many=True)
                    }
                ),
                description='Список рекомендованных товаров и других товаров. '
                            'Поле available = True если количество товаров превышает 0. '
                            'В случае, если идёт фильтрация по категории т.е '
                            'ендпоинт category/<str:category>/, то возвращается '
                            'вместо recommended_goods и other_goods только 1: '
                            '"goods" без изменения самой структуры возвращаемых данных '
                            'и полей. Поле "rating" равно 0 в случае отсутствия отзывов,'
                            'из которых и формируется рейтинг товара.',
                examples=[
                    OpenApiExample(
                        'Пример в случае отсутствия фильтрации по категории',
                        value={
                            'recommended_goods': [
                                {"id": 1, "image": "image file", "title": "string",
                                 "price": "3453454", "rating": "3", "available": True},
                            ],
                            'other_goods': [
                                {"id": 2, "image": "image file", "title": "string",
                                 "price": "100", "rating": "5", "available": True},
                            ]
                        },
                    ),
                    OpenApiExample(
                        'Пример в случае фильтрации по категории',
                        value={
                            'goods': [
                                {"id": 1, "image": "image file", "title": "string",
                                 "price": "3453454", "rating": "3", "available": True},
                                {"id": 2, "image": "image file", "title": "string",
                                 "price": "100", "rating": "5", "available": True}
                            ],
                        },
                    )
                ]
            ),
        }
    )
    def get(self, request, *args, **kwargs):
        """
        Для формирования списка товаров для пользователя
        """
        queryset = Goods.objects.all().select_related('category').only(
            'image', 'title', 'price', 'rating', 'category__title'
        )
        category = self.kwargs.get('category')
        title = self.request.query_params.get('title', None)
        if title:
            queryset = queryset.filter(title__icontains=title)
        if title or category:
            # если пользователь фильтрует товары по категории или по названию --> он не просто
            # просматривает список всех товаров, а пришёл с какой-то конкретной целью и
            # просматривает определённый диапазон товаров --> предлагаем ему
            # отфильтровать по цене
            allowable_price = self.request.query_params.get('price', None)
            if allowable_price:
                min_val, max_val = map(float, allowable_price.split(';'))
                queryset = queryset.filter(price__gte=min_val, price__lte=max_val)

        if not category:
            # если не фильтрует по категориям --> сортируем результат по товарам с теми категориями,
            # с которыми пользователь уже покупал какие-то товары
            recommended_goods = self.get_recommended_goods(queryset)
            other_goods = queryset.exclude(id__in=[
                goods.id for goods in recommended_goods
            ]).order_by('-times_bought')

            recommended_goods_data = GoodsListSerializer(recommended_goods,
                                                         many=True).data
            other_goods_data = GoodsListSerializer(other_goods,
                                                   many=True).data

            return Response({
                'recommended_goods': recommended_goods_data,
                'other_goods': other_goods_data
            }, status=status.HTTP_200_OK)

        queryset = (Goods.objects.filter(category__title__iexact=category).
                    order_by('-times_bought'))
        goods_data = GoodsListSerializer(queryset, many=True).data
        return Response({'goods': goods_data}, status=status.HTTP_200_OK)


class GoodsDetailView(RetrieveAPIView):
    serializer_class = GoodsDetailSerializer
    queryset = Goods.objects.all()


class CommentCreateView(CreateAPIView):
    """
    Для создания комментариев.
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated,
                          permissions.IsGoodsBoughtByUser]

    @extend_schema(
        description='Поля "author_name" и "author_profile_picture" не требуются, '
                    'достаточно body(опциональное поле), rating (int от 1 до 5) и goods (id товара)'
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        Для определения имени автора комментария и его аватара делаем запрос
        в другой микросервис. Решили это дело пока не кешировать, т.к. отзывы -
        достаточно редкое явление со стороны 1 конкретного пользователя, нет смысла
        кешировать на несколько дней т.к из user_service берём динамические данные:
        имя и аватар.
        :return:
        """
        data = request.data
        base_uri = self.request.build_absolute_uri('/')
        relative_url = f'users/{request.user.id}/representational-data/'
        url = f'{base_uri}{relative_url}'
        response = requests.get(url, timeout=8)
        if response.status_code == status.HTTP_200_OK:
            response_data = response.json()  # {'first_name': 'str', 'profile_picture': 'img'}
            user_data = {'author_name': response_data['first_name'],
                         'author_profile_picture': response_data['profile_picture']}
            full_data = {**data, **user_data}
            serializer = self.get_serializer(data=full_data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CommentUpdateDeleteView(mixins.DestroyModelMixin,
                              GenericAPIView):
    serializer_class = CommentUpdateSerializer
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticated, permissions.IsAuthor]

    @extend_schema(description='Поле body опциональное')
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)