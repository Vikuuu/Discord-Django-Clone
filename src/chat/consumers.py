import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import PrivateChatMessage, PrivateChat
from django.contrib.auth import get_user_model


class PrivateChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # join room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)

        private_chat_id = data["data"]["private_chat_id"]
        sent_to_id = data["data"]["sent_to_id"]
        name = data["data"]["name"]
        body = data["data"]["body"]

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "body": body,
                "name": name,
            },
        )

        await self.save_message(private_chat_id, body, sent_to_id)

    async def chat_message(self, event):
        body = event["body"]
        name = event["name"]

        await self.send(
            text_data=json.dumps(
                {
                    "body": body,
                    "name": name,
                }
            )
        )

    @sync_to_async
    def save_message(self, private_chat_id, body, sent_to_id):
        user = self.scope["user"]
        private_chat_instance = PrivateChat.objects.get(id=private_chat_id)
        sent_to_instance = get_user_model().objects.get(id=sent_to_id)
        PrivateChatMessage.objects.create(
            private_chat=private_chat_instance,
            body=body,
            sent_to=sent_to_instance,
            created_by=user,
        )
