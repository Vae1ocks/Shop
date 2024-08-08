from django.urls import path

from .views import *

urlpatterns = [
    path('orders/', OrdersListView.as_view()),
    path('order-create/', OrderCreateView.as_view()),
    # path('order/success/?=<int:order_id>/', OrderPaymentSuccessView.as_view(), name='order_success'),
    path('status/', PaymentStatusView.as_view()),
]
