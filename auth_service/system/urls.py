from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('api/auth/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/auth/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    path('api/auth/', include('authentication.urls')),

    path('api/token/verify/', TokenRefreshView.as_view(), name='token-verify'),
    path('auth/admin/', admin.site.urls),
]
