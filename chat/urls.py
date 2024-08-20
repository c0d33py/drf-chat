from django.urls import include, path
from rest_framework import routers

from .views import *

router = routers.SimpleRouter()
router.register('chatrooms', ChatRoomViewSet)
router.register('messages', MessageViewSet)

urlpatterns = [
    path('users/', UserListAPIView.as_view()),
    path('chats/', UserChatsListAPIView.as_view()),
    path('', include(router.urls)),
]
