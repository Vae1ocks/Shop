"""
Создание заказа
"""

from rest_framework import generics, status, permissions
from rest_framework.response import Response

from django.conf import settings
from yookassa import Configuration, Payment

from payment.models import Order, OrderItem
from payment.serializers.payment.serializers import BasketItemDataSerializer


Configuration.account_id = settings.YOOKASSA_SHOP_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY


class OrderCreateView(generics.CreateAPIView):
    """ Создание заказа """
    serializer_class = BasketItemDataSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = BasketItemDataSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        order = Order.objects.create(user=request.user.id, status='waiting_for_data')
        return Response({
            'order': serializer.data,
        }, status=status.HTTP_201_CREATED)


class OrderPaymentView(generics.GenericAPIView):
    """ Страница успешного платежа """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        order_id = request.session.get('order_id')
        order = Order.objects.get(pk=order_id)
        order.status = 'paid'
        order.save()
        return Response({'detail': 'Оплата прошла успешно.'}, status=status.HTTP_200_OK)