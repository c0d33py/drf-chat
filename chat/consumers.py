import json
import logging
from datetime import datetime

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .models import ChatRoom, DeliveryReceipt, Message

User = get_user_model()
logger = logging.getLogger(__name__)


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs'].get('room_id')
        self.user = self.scope['user']

        if not self.user.is_authenticated:
            await self.close()
            return

        self.chat_room = await self.get_check_chat_room(self.room_id)

        # Join room group
        await self.channel_layer.group_add(self.room_id, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_id, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'send_message':
            await self.handle_send_message(data)
        elif action == 'typing':
            await self.handle_typing(data)
        elif action == 'delivery_receipt':
            await self.handle_delivery_receipt(data)

    async def handle_send_message(self, data):
        content = data.get('content')
        content_type = data.get('content_type')

        message = await self.create_message(self.user.id, content, content_type)

        # Broadcast message to room group
        await self.channel_layer.group_send(
            self.room_id,
            {
                'type': 'chat_message',
                'message': message.content,
                'sender': message.sender.id,
                'timestamp': message.timestamp.isoformat(),
                'content_type': message.content_type,
            },
        )

    async def handle_typing(self, data):
        is_typing = data.get('is_typing')

        # Broadcast typing status to room group
        await self.channel_layer.group_send(
            self.room_id,
            {'type': 'typing_status', 'user': self.user.id, 'is_typing': is_typing},
        )

    async def handle_delivery_receipt(self, data):
        message_id = data.get('message_id')
        delivered = data.get('delivered')
        read = data.get('read')

        await self.update_delivery_receipt(message_id, self.user.id, delivered, read)

        # Broadcast delivery status to room group
        await self.channel_layer.group_send(
            self.room_id,
            {
                'type': 'delivery_status',
                'message_id': message_id,
                'delivered': delivered,
                'read': read,
                'user': self.user.id,
            },
        )

    async def delivery_status(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    'type': 'delivery_status',
                    'message_id': event['message_id'],
                    'delivered': event['delivered'],
                    'read': event['read'],
                    'user': event['user'],
                }
            )
        )

    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    'type': 'chat_message',
                    'message': event['message'],
                    'sender': event['sender'],
                    'timestamp': event['timestamp'],
                    'content_type': event['content_type'],
                }
            )
        )

    async def typing_status(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    'type': 'typing_status',
                    'user': event['user'],
                    'is_typing': event['is_typing'],
                }
            )
        )

    @database_sync_to_async
    def create_message(self, user_id, content, content_type):
        user = User.objects.get(id=user_id)
        chat_room = ChatRoom.objects.get(id=self.room_id)
        return Message.objects.create(
            chat_room=chat_room, sender=user, content=content, content_type=content_type
        )

    @database_sync_to_async
    def update_delivery_receipt(self, message_id, user_id, delivered, read):
        message = Message.objects.get(id=message_id)
        receiver = User.objects.get(id=user_id)
        receipt, created = DeliveryReceipt.objects.get_or_create(
            message=message, receiver=receiver
        )
        if delivered:
            receipt.delivered_at = datetime.now()
        if read:
            receipt.read_at = datetime.now()
            message.is_read = True
            message.read_at = datetime.now()
        receipt.save()
        message.save()

    @database_sync_to_async
    def get_check_chat_room(self, room_id):
        return get_object_or_404(ChatRoom, id=room_id)
