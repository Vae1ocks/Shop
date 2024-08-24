from django.urls import path

from .views import *


urlpatterns = [
    path('social/vk/security/', VKSecurity.as_view()),
    path('social/vk/login/', VkAuth.as_view()),
]
