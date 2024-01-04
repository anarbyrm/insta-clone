from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class MessageStatusType(models.TextChoices):
    PENDING = "PENDING", "Pending"
    SENT = "SENT", "Sent"
    RECEIVED = "RECEIVED", "Received"
    READ = "READ", "Read"


class Message(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="messages_sent"
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="messages_received"
    )
    text = models.TextField()
    status = models.CharField(
        max_length=10,
        choices=MessageStatusType.choices,
        default=MessageStatusType.PENDING
    )
    sent_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sender.username}: {self.text[:50]}"
