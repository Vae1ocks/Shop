from django.urls import path
from . import consumers


websocket_urlpatterns = [
    path('ws/chats/',
         consumers.ChatSupportConsumer.as_asgi()),
]
