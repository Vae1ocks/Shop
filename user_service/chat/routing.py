from django.urls import path
from . import consumers


websocket_urlpatterns = [
    path("ws/chats/<int:pk>/", consumers.PersonalChatConsumer.as_asgi()),
    path("ws/chats/", consumers.ChatSupportConsumer.as_asgi()),
]
