"""
Serializer for Friend Models.
"""

from rest_framework import serializers
from friend.models import FriendRequest


class FriendRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = FriendRequest
        fields = ["sender", "receiver"]

    def create(self, validated_data):
        sender = validated_data["sender"]
        receiver = validated_data["receiver"]

        friend_request = FriendRequest.objects.create(
            sender=sender,
            receiver=receiver,
            status=FriendRequest.Status.PENDING,
        )
        friend_request.save()

        return friend_request

    def update(self, instance, validated_data):
        instance.status = self.context.get("status")
        instance.is_active = False

        instance.save()

        return instance
