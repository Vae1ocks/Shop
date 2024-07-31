from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('api/store/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/store/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/store/', include('store.urls', namespace='store')),
    path('api/basket/', include('basket.urls', namespace='basket')),
    path('admin/', admin.site.urls)
]
