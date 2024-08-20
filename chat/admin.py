from django.contrib import admin

from .models import ChatRoom, DeliveryReceipt, Message

admin.site.register(DeliveryReceipt)


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    """ChatRoomAdmin"""

    list_display = ['id']
    search_fields = ['id']
    list_per_page = 20


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """MessageAdmin"""

    list_display = ['id', 'timestamp']
    search_fields = ['id', 'chatroom_id', 'sender']
    list_per_page = 20
