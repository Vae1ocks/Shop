from django.urls import path

from .views import *


urlpatterns = [
    path('social/google/', GoogleAuth.as_view()),
    path('social/vk/security/', VKSecurity.as_view()),
    path('social/vk/login/', VkAuth.as_view()),
    path('social/yandex/', YandexAuth.as_view()),
]
