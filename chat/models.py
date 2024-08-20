import uuid

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class ChatRoom(models.Model):
    """ChatRoom model representing a chat room in the application."""

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True
    )
    participants = models.ManyToManyField(User, related_name='chat_rooms')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'chat'
        verbose_name = 'chat room'
        verbose_name_plural = 'chat rooms'

    def __str__(self):
        return str(self.id)

    @staticmethod
    def get_or_create_one_on_one_room(user1, user2):
        """Get or create a one-on-one chat room between two users."""
        room = (
            ChatRoom.objects.filter(participants=user1)
            .filter(participants=user2)
            .first()
        )
        if room:
            return room
        room = ChatRoom.objects.create()
        room.participants.add(user1, user2)
        return room


class Message(models.Model):
    """Message model representing a message in a chat room."""

    TEXT = 'text'
    IMAGE = 'image'
    VIDEO = 'video'
    FILE = 'file'
    CONTENT_TYPE_CHOICES = [
        (TEXT, 'Text'),
        (IMAGE, 'Image'),
        (VIDEO, 'Video'),
        (FILE, 'File'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chat_room = models.ForeignKey(
        ChatRoom, on_delete=models.CASCADE, related_name='messages'
    )
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField(blank=True, null=True)
    content_type = models.CharField(
        max_length=10, choices=CONTENT_TYPE_CHOICES, default=TEXT
    )
    file = models.FileField(upload_to='chat_files/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    delivered_at = models.DateTimeField(blank=True, null=True)
    read_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        app_label = 'chat'
        verbose_name = 'message'
        verbose_name_plural = 'messages'
        ordering = ['-timestamp']

    def __str__(self):
        return f'Message {self.id} in {self.chat_room}'


class DeliveryReceipt(models.Model):
    """DeliveryReceipt model representing the delivery receipt of a message."""

    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name='delivery_receipts'
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='delivery_receipts'
    )
    delivered_at = models.DateTimeField(blank=True, null=True)
    read_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        app_label = 'chat'
        verbose_name = 'Delivery Receipt'
        verbose_name_plural = 'Delivery Receipts'
        ordering = ['-delivered_at']

    def __str__(self):
        return f'Receipt for {self.message.id} to {self.receiver}'
