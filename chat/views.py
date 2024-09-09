from django.contrib.auth import get_user_model
from django.db.models import Max
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import ChatRoom, Message
from .pagination import StandardResultsSetPagination
from .serializers import ChatRoomSerializer, MessageSerializer, UserSerializer

User = get_user_model()


class UserListAPIView(generics.ListAPIView):
    """List for managing User, providing List operations with authentication required."""

    permission_classes = [IsAuthenticated]
    queryset = (
        User.objects.filter(is_active=True)
        .select_related('profile')
        .order_by('-username')
    )
    serializer_class = UserSerializer
    pagination_class = StandardResultsSetPagination
    search_fields = ['id', 'username', 'email']

    def get_serializer(self, *args, **kwargs):
        exclude_fields = ['last_message']
        return super().get_serializer(exclude=exclude_fields, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().exclude(id=self.request.user.id)


class ChatRoomViewSet(viewsets.ModelViewSet):
    """Viewset for managing chat rooms, providing CRUD operations with authentication required."""

    permission_classes = [IsAuthenticated]
    queryset = ChatRoom.objects.all().order_by('-id')
    serializer_class = ChatRoomSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """Filter chat rooms to those involving the authenticated user."""
        queryset = super().get_queryset()
        return queryset.filter(participants=self.request.user).order_by('-id')


class MessageViewSet(viewsets.ModelViewSet):
    """A viewset for viewing and editing message instances."""

    queryset = Message.objects.select_related('sender', 'chat_room')
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """
        Optionally restricts the returned messages to those in the chat rooms
        involving the authenticated user.
        """
        queryset = super().get_queryset()
        return queryset.filter(chat_room__participants=self.request.user).order_by(
            '-timestamp'
        )

    @action(detail=True, methods=['get'])
    def chat(self, request, pk=None):
        """
        Get messages from a specific chat between the authenticated user and another user.
        """
        chat_user_id = pk
        messages = self.get_queryset().filter(chat_room__participants__id=chat_user_id)

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(messages, request)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['delete'])
    def clear_chat(self, request, pk=None):
        """
        Clear all messages for a specific chat user.
        """
        chat_user_id = pk
        deleted_count, _ = (
            self.get_queryset()
            .filter(chat_room__participants__id=chat_user_id)
            .delete()
        )
        return Response(
            {'detail': f'{deleted_count} messages deleted.'},
            status=status.HTTP_204_NO_CONTENT,
        )


class UserChatsListAPIView(generics.ListAPIView):
    """Retrieve and list users connected to the authenticated user, ordered by the most recent message timestamp."""

    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    pagination_class = StandardResultsSetPagination
    search_fields = ['id', 'username', 'email']

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        chat_rooms = ChatRoom.objects.filter(participants=user)

        connected_users = (
            User.objects.select_related('profile')
            .filter(chat_rooms__in=chat_rooms)
            .exclude(id=user.id)
            .annotate(latest_message_timestamp=Max('messages__timestamp'))
            .order_by('-latest_message_timestamp')
            .distinct()
        )
        return connected_users
