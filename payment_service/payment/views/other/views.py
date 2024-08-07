"""
Создание заказа
"""

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.shortcuts import reverse
from django.core.exceptions import ObjectDoesNotExist

from django.conf import settings
from yookassa import Configuration, Payment

from payment.models import Order, OrderItem
from payment.serializers.payment.serializers import BasketItemDataSerializer
from payment.serializers.other.serializers import *


Configuration.account_id = settings.YOOKASSA_SHOP_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY


class OrdersListView(generics.ListAPIView):
    serializer_class = OrderListSerializer
    queryset = Order.objects.all()


class OrderCreateView(generics.GenericAPIView):
    """ Создание заказа """
    serializer_class = OrderCreateSerializer
    permission_classes = [permissions.AllowAny]

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
                    'value': order.get_total_price(),
                    'currency': 'RUB',
                },
                'confirmation': {
                    'type': 'redirect',
                    'return_url': request.build_absolute_uri(reverse('payment:order_success', kwargs={'order_id': order.id})),
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


class OrderPaymentSuccessView(generics.GenericAPIView):
    """ Страница успешного платежа """
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        order_id = kwargs['order_id']
        order = Order.objects.get(pk=order_id)
        order.status = 'paid'
        order.save()
        del request.session['payment_id']
        return Response({'detail': 'Оплата прошла успешно.'}, status=status.HTTP_200_OK)


class CheckPaymentStatusView(generics.GenericAPIView):
    """ Проверка статуса оплаты """
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        payment_id = request.session.get('payment_id')
        if payment_id:
            try:
                payment_status = Payment.find_one(payment_id).status
                return Response({'status': payment_status}, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({'status': 'Платеж не найден'}, status=status.HTTP_400_BAD_REQUEST)