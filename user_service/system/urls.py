from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('api/user/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/user/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    path('api/user/', include('user.urls', namespace='user')),

    path('api/user/login', TokenObtainPairView.as_view()),
    path('admin/', admin.site.urls),

]
