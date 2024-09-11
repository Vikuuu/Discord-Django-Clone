"""
Middleware for connecting DRF and Channels.
"""

from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth import get_user_model
from user.utils import JwtTokens


@database_sync_to_async
def get_user(token_key):
    """Returns user instance by decoding the JWT token."""
    try:
        user_id = JwtTokens.decode_access_token(token_key)
        return get_user_model().objects.get(pk=user_id)

    except Exception as e:
        return AnonymousUser


class JWTAuthMiddleware(BaseMiddleware):
    """
    Authentication middleware to help the channels know who
    the user is.
    """

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        print(f"scope query string: {scope["query_string"]}")
        query = dict(
            (x.split("=") for x in scope["query_string"].decode().split("&"))
        )
        token_key = query.get("token")
        print(token_key)

        if token_key:
            scope["user"] = await get_user(token_key)
        else:
            scope["user"] = AnonymousUser()

        return await super().__call__(scope, receive, send)
