"""
User Required Database.
"""

from django.db import models
from django.conf import settings
import os
import uuid


def user_profile_image_file_path(instance, filename):
    """Generate file path for user profile image."""
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid.uuid4()}{ext}"

    return os.path.join("uploads", "profile", filename)


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


class UserProfile(models.Model):
    """User Profile Model."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    photo = models.ImageField(
        null=True, upload_to=user_profile_image_file_path
    )

    def __str__(self):
        return f"{self.user.username}'s profile"
