from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db import transaction

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.api.serializers import ProfileSerializer
from accounts.models import FriendshipRequest, FriendshipResponseType, Profile
from config.permissions import IsOwner

User = get_user_model()


class UserProfileView(RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated, IsOwner)

    def get_object(self):
        username = self.request.query_params.get("username")

        if username:
            profile = get_object_or_404(Profile, user__username=username)
            self.check_object_permissions(self.request, profile)
            return profile

        return None


class FriendRequestView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        user = get_object_or_404(User, username=username)

        if user == request.user:
            return Response({"message": "cannot sent request to yourself"},
                            status=status.HTTP_400_BAD_REQUEST)

        if user in request.user.user_profile.friends.all():
            return Response({"message": "%s is already your friend" % username},
                            status=status.HTTP_400_BAD_REQUEST)

        user_request = FriendshipRequest.objects.filter(
            sender=user,
            receiver=request.user
        ).first()

        if user_request:
            with transaction.atomic():
                user_request.response = FriendshipResponseType.ACCEPT
                user_request.save(update_fields=["response"])

                user.user_profile.friends.add(request.user)
                request.user.user_profile.friends.add(user)

                return Response({"message": "Accepted the request from '%s'" % username},
                            status=status.HTTP_200_OK)

        # new request created
        _friend_request, created = FriendshipRequest.objects.get_or_create(
            sender=request.user,
            receiver=user
        )
        if created:
            return Response({"message": "Friendship request sent to '%s'" % username},
                             status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Friendship request has already been sent to '%s'" % username},
                             status=status.HTTP_400_BAD_REQUEST)
