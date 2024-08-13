"""
Создание заказа
"""

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.shortcuts import reverse
from django.core.exceptions import ObjectDoesNotExist
from drf_spectacular.utils import extend_schema
from decimal import Decimal
from django.contrib.auth import get_user_model

from django.conf import settings
from yookassa import Configuration, Payment, Webhook

from payment.models import Order, OrderItem
from payment.serializers.other.serializers import *

Configuration.account_id = settings.YOOKASSA_SHOP_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY


class OrdersListView(generics.ListAPIView):
    """ Список всех заказов """
    serializer_class = OrderListSerializer
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAdminUser]


class OrderCreateView(generics.GenericAPIView):
    """ Создание заказа """
    serializer_class = OrderCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(description='API создания заказа. В нем указываются товары, которые пользователь хочет купить и '
                               'юзера, который совершает покупку.'
                   )
    def post(self, request, *args, **kwargs):
        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = Order.objects.create(user=request.user.id, status='waiting_for_data')
        for item in serializer.validated_data['goods']:
            OrderItem.objects.create(order=order, **item)
        # create Payment for yookassa.
        payment = Payment.create(
            {
                'amount': {
                    'value': Decimal(order.get_total_price()),
                    'currency': 'RUB',
                },
                'confirmation': {
                    'type': 'redirect',
                    # 'return_url': request.build_absolute_uri(
                    #     reverse('payment:order_success', kwargs={'order_id': order.id})),
                    'return_url': 'http://31.129.108.243/api/payment/docs/'
                },
                'capture': True,
                'test': True,
                'description': f'Заказ №{order.id}'
            }
        )
        confirmation_url = payment.confirmation.confirmation_url
        request.session['payment_id'] = payment.id
        return Response({
            'confirmation': confirmation_url,
            'order_id': order.id
        }, status=status.HTTP_201_CREATED)

# # TODO: Переделать. Добавить в модель payment_id, при создании заказа, добавлять и id payment
# # TODO: в url success/<str:payment_id>/ мы принимаем payment_id, проверяем статус оплаты и изменяем у заказа статус
# class OrderPaymentSuccessView(generics.GenericAPIView):
#     """ Страница успешного платежа """
#     permission_classes = [permissions.IsAuthenticated]
#
#     def get(self, request, *args, **kwargs):
#         order_id = kwargs['order_id']
#         order = Order.objects.get(pk=order_id)
#         order.status = 'paid'
#         order.save()
#         del request.session['payment_id']
#         return Response({'detail': 'Оплата прошла успешно.'}, status=status.HTTP_200_OK)

# TODO: https://yookassa.ru/developers/api#webhook сделать вебхук
class PaymentStatusView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def get_client_ip_address(request):
        req_headers = request.META
        x_forwarded_for_value = req_headers.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for_value:
            ip_addr = x_forwarded_for_value.split(',')[-1].strip()
        else:
            ip_addr = req_headers.get('REMOTE_ADDR')
        return ip_addr

    def post(self, request, *args, **kwargs):
        allowed_ips = [
            '185.71.76.0/27',
            '185.71.77.0/27',
            '77.75.153.0/25',
            '77.75.156.11',
            '77.75.156.35',
            '77.75.154.128/25',
            '2a02:5180::/32'
        ]
        client_ip = self.get_client_ip_address(request)
        if client_ip not in allowed_ips:
            return Response(status=status.HTTP_403_FORBIDDEN)
        response = request.data
        status = response['event'].split('.')[1]
        order_id = int(response['object']['description'].split('№')[1])
        order = Order.objects.get(pk=order_id)
        order.status = status
        return Response({'detail': f'Статус заказа {order.id} - {order.status}'})


class UserOrderListView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user.pk
        orders = Order.objects.filter(user=user)
        serializer = OrderListSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


