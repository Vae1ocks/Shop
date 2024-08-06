from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('payment/api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('payment/api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    path('payment/api/', include('payment.urls', namespace='payment')),
    # path('payment/api/coupons/', include('coupons.urls', namespace='coupons')),

    path('payment/admin/', admin.site.urls),
    path('payment/api/login', TokenObtainPairView.as_view()),
]
