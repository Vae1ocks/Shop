import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

django_asgi_app = get_asgi_application()

from chat.middleware import TokenOrSessionAuthMiddleware
from chat.routing import websocket_urlpatterns

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": TokenOrSessionAuthMiddleware(
            URLRouter(websocket_urlpatterns),
        ),
    }
)
