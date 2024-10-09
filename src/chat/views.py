from django.http import JsonResponse
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework import permissions
from core.backends import JwtAuthentication

from .models import PrivateChat, PrivateChatMessage
from .serializers import (
    PrivateChatListSerializer,
    PrivateChatDetailSerializer,
    PrivateChatMessageSerializer,
)
from django.contrib.auth import get_user_model


@api_view(["GET"])
@authentication_classes([JwtAuthentication])
@permission_classes([permissions.IsAuthenticated])
def private_chat_list(request):
    serializer = PrivateChatListSerializer(
        request.user.conversations.all(), many=True
    )

    return JsonResponse(serializer.data, safe=False)


@api_view(["GET"])
@authentication_classes([JwtAuthentication])
@permission_classes([permissions.IsAuthenticated])
def private_chat_detail(request, pk):
    private_chat = request.user.conversations.get(pk=pk)

    private_chat_serializer = PrivateChatDetailSerializer(
        private_chat, many=False
    )
    messages_serializer = PrivateChatMessageSerializer(
        private_chat.messages.all(), many=True
    )

    return JsonResponse(
        {
            "private_chat": private_chat_serializer.data,
            "private_chat_messages": messages_serializer.data,
        },
        safe=False,
    )


@api_view(["GET"])
@authentication_classes([JwtAuthentication])
@permission_classes([permissions.IsAuthenticated])
def private_chat_start(request, user_id):
    private_chat = PrivateChat.objects.filter(users__in=[user_id]).filter(
        users__in=[request.user.id]
    )

    if private_chat.count() > 0:
        private_chat = private_chat.first()
        return JsonResponse(
            {"success": True, "private_chat_id": private_chat.id},
        )
    else:
        user = get_user_model().objects.get(pk=user_id)
        private_chat = PrivateChat.objects.create()

        private_chat.users.add(request.user)
        private_chat.users.add(user)

        return JsonResponse(
            {"success": True, "private_chat_id": private_chat.id}
        )
