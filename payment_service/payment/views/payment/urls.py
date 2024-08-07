from django.urls import path
from .views import *
from payment.webhooks import StripeWebhook

urlpatterns = [
    path('payment/stripe/create/', PaymentCreateView.as_view(), name='stripe_payment_create'),
    path('payment/success', PaymentSuccessView.as_view(), name='payment_success'),
    path('payment/cancelled', PaymentCanceledView.as_view(), name='payment_canceled'),
    # path('stripe/webhook/', StripeWebhook.as_view(), name='stripe_webhook')
]