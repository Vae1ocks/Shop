from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('payment/api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('payment/api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    path('payment/', include('payment.urls', namespace='payment')),
    path('coupons/', include('coupons.urls', namespace='coupons')),

    path('admin/', admin.site.urls),
]
