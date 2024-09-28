import stripe
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.status import *
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Order


class StripeWebhook(GenericAPIView):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
        event = None

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except ValueError as e:
            return Response(status=HTTP_400_BAD_REQUEST)
        except stripe.error.SignatureVerificationError as e:
            return Response(status=HTTP_400_BAD_REQUEST)

        if event.type == "checkout.session.completed":
            session = event.data.object
            if session.mode == "payment" and session.payment_status == "paid":
                try:
                    order = Order.objects.get(id=session.client_reference_id)
                except Order.DoesNotExist:
                    return Response(status=HTTP_404_NOT_FOUND)
                order.status = "succeeded"
                order.save()
        return Response(status=HTTP_200_OK)
