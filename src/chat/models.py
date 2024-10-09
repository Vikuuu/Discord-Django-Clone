from django.db import models
from django.conf import settings


class PrivateChat(models.Model):
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="conversations"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class PrivateChatMessage(models.Model):
    private_chat = models.ForeignKey(
        PrivateChat, related_name="messages", on_delete=models.CASCADE
    )
    body = models.TextField()
    sent_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="received_messages",
        on_delete=models.CASCADE,
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="sent_messages",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
