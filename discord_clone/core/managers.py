"""
Custom Managers for the models.
"""

from django.contrib.auth.models import BaseUserManager


class UserAccountManager(BaseUserManager):
    """Custom user models manager."""

    def create_user(self, username, email, password=None, **extra_fields):
        """Create, save and return new User."""
        if not username:
            raise ValueError("User must have an username.")
        if not email:
            raise ValueError("User must have an email.")

        username = username.lower()
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password):
        """Create, save and return new superuser."""
        user = self.create_user(username, email)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user
