"""
Utility functions code.
"""

import jwt
from django.utils import timezone
from datetime import timedelta
from rest_framework import exceptions


class JwtTokens:
    """Utility class for creating JSON Tokens for authentication."""

    @staticmethod
    def create_access_token(id):
        now = timezone.now()
        return jwt.encode(
            {
                "user_id": str(id),
                "exp": now + timedelta(seconds=300),
                "iat": now,
            },
            "access_secret",
            algorithm="HS256",
        )

    @staticmethod
    def create_refresh_token(id):
        now = timezone.now()
        return jwt.encode(
            {
                "user_id": str(id),
                "exp": now + timedelta(days=7),
                "iat": now,
            },
            "refresh_secret",
            algorithm="HS256",
        )

    @staticmethod
    def decode_access_token(token):
        try:
            payload = jwt.decode(token, "access_secret", algorithms="HS256")
            return payload["user_id"]

        except Exception as e:
            raise exceptions.AuthenticationFailed(f"Unauthenticated {str(e)}")

    @staticmethod
    def decode_refresh_token(token):
        try:
            payload = jwt.decode(token, "refresh_secret", algorithms="HS256")
            return payload["user_id"]

        except Exception as e:
            raise exceptions.AuthenticationFailed(f"Unauthenticated {str(e)}")
