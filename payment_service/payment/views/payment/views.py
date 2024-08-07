import stripe.checkout
from rest_framework.generics import *
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.urls import reverse
from django.shortcuts import get_object_or_404, reverse
from decimal import Decimal
from drf_spectacular.utils import extend_schema, inline_serializer, \
    OpenApiResponse, OpenApiExample

from payment.serializers.payment import serializers
from payment.models import Order, OrderItem


stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


# class OrderCreateView(GenericAPIView):
#     def post(self, request, *args, **kwargs):
#         serializer = serializers.BasketItemDataSerializer(data=request.data, many=True)
#         if serializer.is_valid():
#             order = Order.objects.create(user=request.user.id,
#                                          status='waiting_for_data')
#             for item in serializer.data:
#                 goods_data = item.pop('goods')
#                 OrderItem.objects.create(**item, **goods_data)
#             request.session['order_id'] = order.id
#             url = reverse('payment:process')
#             return Response(status=HTTP_308_PERMANENT_REDIRECT,
#                             headers={'Location': url})
#         return Response(serializer.errors, HTTP_400_BAD_REQUEST)


class PaymentCreateView(GenericAPIView):
    serializer_class = serializers.BasketItemDataSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(request=serializers.BasketItemDataSerializer(many=True))
    def post(self, request, *args, **kwargs):
        serializer = serializers.BasketItemDataSerializer(data=request.data, many=True)
        if serializer.is_valid():
            order = Order.objects.create(user=request.user.id,
                                         status='waiting_for_data')
            for item in serializer.data:
                goods_data = item.pop('goods')
                OrderItem.objects.create(order=order, **item, **goods_data)

            success_url = request.build_absolute_uri(reverse('payment:payment_success'))
            cancel_url = request.build_absolute_uri(reverse('payment:payment_canceled'))

            session_data = {
                'mode': 'payment',
                'client_reference_id': order.id,
                'success_url': success_url,
                'cancel_url': cancel_url,
                'line_items': []
            }
            for item in order.items.all():
                session_data['line_items'].append(
                    {
                        'price_data': {
                            'unit_amount': int(item.price * Decimal('100')),
                            'currency': 'rub',
                            'product_data': {
                                'name': item.goods_title
                            }
                        },
                        'quantity': item.amount
                    }
                )

                session = stripe.checkout.Session.create(**session_data)
                print(session.url)
                return Response(status=HTTP_301_MOVED_PERMANENTLY,
                                headers={'Location': session.url})
        return Response(serializer.errors, HTTP_400_BAD_REQUEST)


class PaymentSuccessView(GenericAPIView):
    @extend_schema(description='В случае успешной оплаты платёжный сервис осуществит '
                               'redirect на этот url',
                   responses={
                       200: OpenApiResponse(
                           inline_serializer(
                               'Success-Payment',
                               fields={'detail': serializers.CharField()}
                           ),
                           examples=[
                               OpenApiExample(
                                   'В случае успешной оплаты',
                                   value={
                                       'detail': 'Оплата проведена успешно'
                                   }
                               )
                           ]
                       )
                   }
                   )
    def get(self, request, *args, **kwargs):
        return Response({'detail': 'Оплата проведена успешно'}, HTTP_200_OK)


class PaymentCanceledView(GenericAPIView):

    @extend_schema(description='В случае неудачной оплаты платёжный сервис осуществит '
                               'redirect на этот url',
                   responses={
                       200: OpenApiResponse(
                           inline_serializer(
                               'Canceled-Payment',
                               fields={'detail': serializers.CharField()}
                           ),
                           examples=[
                               OpenApiExample(
                                   'В случае неудачной оплаты',
                                   value={
                                       'detail': 'Оплата не проведена'
                                   }
                               )
                           ]
                       )
                   }
                   )
    def get(self, request):
        return Response({'detail': 'Оплата не проведена'}, HTTP_422_UNPROCESSABLE_ENTITY)