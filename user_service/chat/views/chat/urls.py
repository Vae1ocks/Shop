from django.urls import path
from .views import *

urlpatterns = [
    path("create/", ChatCreateView.as_view(), name="chat_create"),
    path("<int:pk>/", ChatRetrieveView.as_view(), name="chat_detail"),
]
