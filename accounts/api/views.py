from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from accounts.api.serializers import ProfileSerializer
from accounts.models import FrendshipRequest, Profile


class ProfileView(RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        """
        Only returns profile of current user
        """
        queryset = self.get_queryset()
        return queryset.filter(user=self.request.user).first()
