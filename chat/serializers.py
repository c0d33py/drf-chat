from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import ChatRoom, Message

User = get_user_model()


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed."""

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        exclude = kwargs.pop('exclude', None)
        super().__init__(*args, **kwargs)

        if fields:
            # Only include the specified fields
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
        elif exclude:
            # Exclude the specified fields
            for field_name in exclude:
                self.fields.pop(field_name)


class UserSerializer(DynamicFieldsModelSerializer):
    full_name = serializers.CharField(source='get_full_name')
    profile_image = serializers.SerializerMethodField()
    gender = serializers.CharField(source='profile.get_gender_display')
    date_of_birth = serializers.DateField(source='profile.dob')
    last_message = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'full_name',
            'email',
            'date_of_birth',
            'gender',
            'profile_image',
            'last_login',
            'date_joined',
            'last_message',
        ]

    def get_last_message(self, instance):
        current_user = self.context['request'].user
        chat_room = (
            ChatRoom.objects.filter(participants=current_user)
            .filter(participants=instance)
            .first()
        )
        try:
            last_message = chat_room.messages.order_by('-timestamp').first()
            return {
                'chat_room': str(chat_room.id),
                'message': last_message.content,
                'timestamp': last_message.timestamp,
                'is_read': last_message.is_read,
            }
        except AttributeError:
            return None

    def get_profile_image(self, user):
        request = self.context.get('request')
        try:
            image_path = user.profile.image.url
            return request.build_absolute_uri(image_path)
        except AttributeError:
            return None


class ChatRoomSerializer(serializers.ModelSerializer):
    """Serializer for the ChatRoom model."""

    class Meta:
        model = ChatRoom
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for the Message model."""

    sender_name = serializers.CharField(source='sender.username')

    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['is_read', 'delivered_at', 'read_at']

    def create(self, validated_data):
        request = self.context.get('request')
        current_user = request.user
        chat_user_id = request.data.get('user_id')
        chat_room = ChatRoom.objects.filter(participants=current_user).get(
            participants__id=chat_user_id
        )
        validated_data['chat_room'] = chat_room
        validated_data['sender'] = current_user
        return super().create(validated_data)
