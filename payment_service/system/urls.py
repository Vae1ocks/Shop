from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('api/payment/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/payment/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    path('payment/', include('payment.urls', namespace='payment')),
    # path('coupons/', include('coupons.urls', namespace='coupons')),

    path('admin/', admin.site.urls),
    path('api/payment/login', TokenObtainPairView.as_view()),
]
