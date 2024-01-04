from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db import transaction

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.api.serializers import FriendRequestSerializer, ProfileSerializer
from accounts.constants import FRIENDSHIP_DEFAULT_RESPONSE
from accounts.models import FriendshipRequest, FriendshipResponseType, Profile
from chat.models import ChatBox
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
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        all_requests = FriendshipRequest.objects.filter(receiver=request.user, 
                                                        response=FRIENDSHIP_DEFAULT_RESPONSE)
        serializer = FriendRequestSerializer(all_requests, many=True)
        data = {
            "requests": serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)

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
                # automatically creates chatbox when friend request accepted
                ChatBox.members.add(request.user, user)

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


class FriendRequestResponseView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        friendship_request = get_object_or_404(FriendshipRequest,
                                               pk=pk,
                                               response=FRIENDSHIP_DEFAULT_RESPONSE)
        if "response" not in request.data:
            return Response({"message": "no valid response for friendship request"},
                            status=status.HTTP_400_BAD_REQUEST)
        
        response = request.data["response"]
        if response == FriendshipResponseType.ACCEPT:
            serializer = FriendRequestSerializer(friendship_request, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)

            with transaction.atomic():
                serializer.save(updated_fields=["response"])
                request.user.user_profile.friends.add(friendship_request.sender)
                friendship_request.sender.user_profile.friends.add(request.user)
                # automatically creates chatbox when friend request accepted
                ChatBox.members.add(request.user, friendship_request.sender)
        elif response == FriendshipResponseType.REJECT:
            friendship_request.delete()

        return Response(serializer.data, status=status.HTTP_200_OK)
