import jwt
from django.utils import timezone
from datetime import timedelta


class JwtTokens:
    """Utility class for creating JSON Tokens for authentication."""

    @staticmethod
    def create_access_token(id):
        now = timezone.now()
        return jwt.encode(
            {
                "user.id": str(id),
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
                "user.id": str(id),
                "exp": now + timedelta(days=7),
                "iat": now,
            },
            "refresh_secret",
            algorithm="HS256",
        )
