from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('auth/api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('auth/api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    path('auth/api/', include('authentication.urls')),

    path('auth/api/token/verify/', TokenRefreshView.as_view(), name='token-verify'),
    path('auth/admin/', admin.site.urls),
]
