"""
Signals to be triggered for Friend Functionality.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from friend.models import FriendList


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_friend_list(sender, instance, created, **kwargs):
    """Creates the friend list when user is created."""
    if created:
        FriendList.objects.create(user=instance)
