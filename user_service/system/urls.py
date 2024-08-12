from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('user/api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('user/api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    path('user/api/', include('user.urls', namespace='user')),

    path('user/api/login', TokenObtainPairView.as_view()),
    path('user/admin/', admin.site.urls)
]
