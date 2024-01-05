from rest_framework import serializers

from chat.models import Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = (
            "sender",
            "receiver",
            "text",
            "status",
            "sent_at",
            "updated_at",
        )
        read_only_fields = (
            "sender",
            "receiver",
            "status",
            "sent_at",
            "updated_at",
        )
