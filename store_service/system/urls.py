from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('store/api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('store/api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    path('store/api/basket/', include('basket.urls', namespace='basket')),
    path('store/api/favorites/', include('favorites.urls'), namespace='favorites'),
    path('store/api/', include('store.urls', namespace='store')),
    path('store/admin/', admin.site.urls),

    path('store/api/login', TokenObtainPairView.as_view()),
]
