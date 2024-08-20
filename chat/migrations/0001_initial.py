import uuid

import django.db.models.deletion as django
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    """Migration for creating the ChatRoom, Message, DeliveryReceipt, and TypingIndicator models."""

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatRoom',
            fields=[
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        db_index=True,
                    ),
                ),
                (
                    'name',
                    models.CharField(
                        max_length=100,
                        blank=True,
                        null=True,
                    ),
                ),
                (
                    'created_at',
                    models.DateTimeField(
                        auto_now_add=True,
                    ),
                ),
                (
                    'participants',
                    models.ManyToManyField(
                        related_name='chat_rooms',
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                'verbose_name': 'chat room',
                'verbose_name_plural': 'chat rooms',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    'content',
                    models.TextField(
                        blank=True,
                        null=True,
                    ),
                ),
                (
                    'content_type',
                    models.CharField(
                        max_length=10,
                        choices=[
                            ('text', 'Text'),
                            ('image', 'Image'),
                            ('video', 'Video'),
                            ('file', 'File'),
                        ],
                        default='text',
                    ),
                ),
                (
                    'file',
                    models.FileField(
                        upload_to='chat_files/',
                        blank=True,
                        null=True,
                    ),
                ),
                (
                    'timestamp',
                    models.DateTimeField(
                        auto_now_add=True,
                    ),
                ),
                (
                    'is_read',
                    models.BooleanField(
                        default=False,
                    ),
                ),
                (
                    'delivered_at',
                    models.DateTimeField(
                        blank=True,
                        null=True,
                    ),
                ),
                (
                    'read_at',
                    models.DateTimeField(
                        blank=True,
                        null=True,
                    ),
                ),
                (
                    'chat_room',
                    models.ForeignKey(
                        related_name='messages',
                        to='chat.ChatRoom',
                        on_delete=django.CASCADE,
                    ),
                ),
                (
                    'sender',
                    models.ForeignKey(
                        related_name='messages',
                        to=settings.AUTH_USER_MODEL,
                        on_delete=django.CASCADE,
                    ),
                ),
            ],
            options={
                'verbose_name': 'message',
                'verbose_name_plural': 'messages',
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='DeliveryReceipt',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'delivered_at',
                    models.DateTimeField(
                        blank=True,
                        null=True,
                    ),
                ),
                (
                    'read_at',
                    models.DateTimeField(
                        blank=True,
                        null=True,
                    ),
                ),
                (
                    'receiver',
                    models.ForeignKey(
                        related_name='delivery_receipts',
                        to=settings.AUTH_USER_MODEL,
                        on_delete=django.CASCADE,
                    ),
                ),
                (
                    'message',
                    models.ForeignKey(
                        related_name='delivery_receipts',
                        to='chat.Message',
                        on_delete=django.CASCADE,
                    ),
                ),
            ],
            options={
                'verbose_name': 'Delivery Receipt',
                'verbose_name_plural': 'Delivery Receipts',
                'ordering': ['-delivered_at'],
            },
        ),
        migrations.CreateModel(
            name='TypingIndicator',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                (
                    'is_typing',
                    models.BooleanField(
                        default=False,
                    ),
                ),
                (
                    'timestamp',
                    models.DateTimeField(
                        auto_now=True,
                    ),
                ),
                (
                    'chat_room',
                    models.ForeignKey(
                        related_name='typing_indicators',
                        to='chat.ChatRoom',
                        on_delete=django.CASCADE,
                    ),
                ),
                (
                    'user',
                    models.ForeignKey(
                        related_name='typing_indicators',
                        to=settings.AUTH_USER_MODEL,
                        on_delete=django.CASCADE,
                    ),
                ),
            ],
            options={
                'verbose_name': 'Typing Indicator',
                'verbose_name_plural': 'Typing Indicators',
                'ordering': ['-timestamp'],
            },
        ),
    ]
