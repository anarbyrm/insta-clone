from django.contrib.auth import get_user_model
from django.db import transaction

from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, UserSerializer
from djoser.conf import settings as djoser_settings

from accounts.models import Profile

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    def perform_create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create_user(**validated_data)
            if djoser_settings.SEND_ACTIVATION_EMAIL:
                user.is_active = False
                user.save(update_fields=["is_active"])
            # create profile with created user instance
            Profile.objects.create(user=user)
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "id",
            "user",
            "bio",
            "photo",
            "total_friends"
        )
        read_only_fields = (
            "id",
            "user",
            "total_friends"
        )
