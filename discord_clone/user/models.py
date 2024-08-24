"""
User Required Database.
"""

from django.db import models
from django.conf import settings


class UserToken(models.Model):
    """Model for storing the current valid tokens."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tokens",
    )
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username}'s Token."
