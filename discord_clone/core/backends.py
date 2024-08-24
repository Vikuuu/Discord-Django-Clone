"""
Custom Backend.
"""

from django.contrib.auth import get_user_model
from rest_framework.authentication import (
    BaseAuthentication,
    get_authorization_header,
)
from user.utils import JwtTokens
from rest_framework.exceptions import AuthenticationFailed


class AuthenticationEmailBackend:
    """Authenticates the user via email."""

    def authenticate(self, request, username=None, password=None):
        try:
            user = get_user_model().objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except (
            get_user_model().DoesNotExist,
            get_user_model().MultipleObjectsReturned,
        ):
            return None

    def get_user(self, user_id):
        try:
            return get_user_model().objects.get(pk=user_id)
        except get_user_model().DoesNotExist:
            return None


class AuthenticationUsernameBackend:
    """Authenticates the user via username."""

    def authenticate(self, request, username=None, password=None):
        try:
            user = get_user_model().objects.get(username=username)
            if user.check_password(password):
                return user
            return None
        except (
            get_user_model().DoesNotExist,
            get_user_model().MultipleObjectsReturned,
        ):
            return None

    def get_user(self, user_id):
        try:
            return get_user_model().objects.get(pk=user_id)
        except get_user_model().DoesNotExist:
            return None


class JwtAuthentication(BaseAuthentication):
    """Authenticates the user using Bearer Token and returns the user related to it."""

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if auth and len(auth) == 2:
            token = auth[1].decode("utf-8")
            id = JwtTokens.decode_access_token(token)

            user = get_user_model().objects.get(pk=id)
            return (user, None)

        raise AuthenticationFailed("Unauthenticated")
