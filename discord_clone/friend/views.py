"""
Views for the Friend functionalality.
"""

from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from core.backends import JwtAuthentication

from django.contrib.auth import get_user_model
from friend.models import FriendRequest, FriendList
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

    serializer_class = FriendRequestSerializer
    authentication_classes = [JwtAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, username):
        receiver = request.user
        sender_username = username
        if sender_username:
            try:
                sender = get_user_model().objects.get(username=sender_username)
                instance = FriendRequest.objects.get(
                    sender=sender, receiver=receiver
                )
                data = {"sender": sender.id, "receiver": receiver.id}
                context = {"status": FriendRequest.Status.ACCEPTED}
                serializer = self.get_serializer(
                    instance, data=data, partial=True, context=context
                )
                serializer.is_valid(raise_exception=True)
                serializer.save()

                # updating the Friend List
                receiver_friend_list, _ = FriendList.objects.get_or_create(
                    user=receiver
                )
                receiver_friend_list.add_friend(sender)
                sender_friend_list, _ = FriendList.objects.get_or_create(
                    user=sender
                )
                sender_friend_list.add_friend(receiver)

                return Response(
                    {"success": "You are now friends!"},
                    status=status.HTTP_202_ACCEPTED,
                )
            except get_user_model().DoesNotExist:
                return Response(
                    {"error": "User not found!"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(
                {"error": "Something went wrong"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class RejectFriendRequestView(generics.GenericAPIView):
    """Reject the Friend Request from the another user."""

    def post(self, request):
        pass


class CancelFriendRequestView(generics.GenericAPIView):
    """Cancel the Sent Friend Request."""

    def post(self, request):
        pass
