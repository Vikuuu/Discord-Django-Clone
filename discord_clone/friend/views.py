"""
Views for the Friend functionalality.
"""

from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from core.backends import JwtAuthentication

from django.contrib.auth import get_user_model
from friend.models import FriendRequest
from friend.serializers import FriendRequestSerializer


class SendFriendRequestView(generics.GenericAPIView):
    """Send a Friend Request to the selected user."""

    serializer_class = FriendRequestSerializer
    authentication_classes = [JwtAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, username):
        sender = request.user
        receiver_username = username
        if receiver_username:
            try:
                receiver = get_user_model().objects.get(
                    username=receiver_username
                )
                data = {"sender": sender.id, "receiver": receiver.id}
                serializer = self.get_serializer(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(
                    {"success": "Friend Request sent successfully"},
                    status=status.HTTP_201_CREATED,
                )
            except get_user_model().DoesNotExist:
                return Response(
                    {"error": "User Does not exists."},
                    status=status.HTTP_404_NOT_FOUND,
                )
        return Response(
            {"error": "Something went wrong"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class AcceptFriendRequestView(generics.GenericAPIView):
    """Accept the Friend Request from the another user."""

    def post(self, request):
        pass


class RejectFriendRequestView(generics.GenericAPIView):
    """Reject the Friend Request from the another user."""

    def post(self, request):
        pass


class CancelFriendRequestView(generics.GenericAPIView):
    """Cancel the Sent Friend Request."""

    def post(self, request):
        pass
