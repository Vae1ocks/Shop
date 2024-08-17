from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model, BACKEND_SESSION_KEY
from django.db import close_old_connections
from django.conf import settings

from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async


@database_sync_to_async
def get_user(id):
    try:
        return get_user_model().objects.get(id=id)
    except get_user_model().DoesNotExist:
        return AnonymousUser()


async def check_token(token):
    try:
        auth_header_type, token = token.split(' ')
        if auth_header_type not in settings.SIMPLE_JWT['AUTH_HEADER_TYPES']:
            return AnonymousUser()
        token_decode = AccessToken(token)
        id = token_decode['user_id']
        return await get_user(id)
    except (InvalidToken, TokenError):
        return AnonymousUser()


class TokenOrSessionAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        close_old_connections()
        headers = dict(scope['headers'])
        token = headers.get(b'authorization')
        if token:
            token = token.decode('utf-8')
            scope['user'] = await check_token(token)
        else:
            inner = AuthMiddlewareStack(self.inner)
            return await inner(scope, receive, send)

        return await self.inner(scope, receive, send)
