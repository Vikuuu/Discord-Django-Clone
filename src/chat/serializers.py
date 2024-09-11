"""
Serializers for models.py
"""

from rest_framework import serializers
from .models import PrivateChat, PrivateChatMessage

from user.serializers import ProfileSerializer


class PrivateChatListSerializer(serializers.ModelSerializer):
    users = ProfileSerializer(many=True, read_only=True)

    class Meta:
        model = PrivateChat
        fields = ["id", "users", "modified_at"]


class PrivateChatDetailSerializer(serializers.ModelSerializer):
    users = ProfileSerializer(many=True, read_only=True)

    class Meta:
        model = PrivateChat
        fields = ["id", "users", "modified_at"]


class PrivateChatMessageSerializer(serializers.ModelSerializer):
    sent_to = ProfileSerializer(many=False, read_only=True)
    created_by = ProfileSerializer(many=False, read_only=True)

    class Meta:
        model = PrivateChatMessage
        fields = ["id", "body", "sent_to", "created_by"]
