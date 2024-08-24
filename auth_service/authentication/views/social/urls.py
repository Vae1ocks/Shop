from django.urls import path

from .views import *


urlpatterns = [

    path('social/vk/', VKLoginView.as_view()),
]
