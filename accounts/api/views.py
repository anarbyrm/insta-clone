from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from accounts.api.serializers import ProfileSerializer
from accounts.models import FrendshipRequest, Profile
from config.permissions import IsOwner


class UserProfileView(RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated, IsOwner)

    def get_object(self):
        username = self.request.query_params.get("username")

        if username:
            profile = get_object_or_404(Profile, user__username=username)
            print(profile)
            self.check_object_permissions(self.request, profile)
            return profile

        return None
