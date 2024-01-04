from django.db import models
from django.conf import settings

from accounts.constants import FRIENDSHIP_DEFAULT_RESPONSE

User = settings.AUTH_USER_MODEL


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="user_profile"
    )
    photo = models.ImageField(
        upload_to="profile_pics",
        null=True,
        blank=True
    )
    bio = models.TextField(
        max_length=250,
        null=True,
        blank=True
    )
    friends = models.ManyToManyField(
        User,
        blank=True
    )

    def __str__(self):
        return f"Profile: {self.user.username}"
    
    @property
    def total_friends(self):
        return self.friends.count()

    @property
    def username(self):
        return self.user.username


class FriendshipResponseType(models.TextChoices):
    ACCEPT = "ACCEPT", "Accept"
    REJECT = "REJECT", "Reject"


class FriendshipRequest(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="requests_sent"
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="requests_received"
    )
    response = models.CharField(
        max_length=10,
        choices=FriendshipResponseType.choices,
        default=FRIENDSHIP_DEFAULT_RESPONSE
    )
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From: {self.sender.username} to: {self.receiver.username}"
