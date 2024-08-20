from consumers import ChatConsumer
from django.urls import path

websocket_urlpatterns = [
    path('ws/chat/<uuid:room_id>/', ChatConsumer.as_asgi()),
]
