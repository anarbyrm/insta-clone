from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from chat.api.serializers import MessageSerializer
from chat.api.pagination import MessagePagination
from chat.models import Message
from config.permissions import IsOwner

User = get_user_model()


class MessageViewSet(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticated, IsOwner)
    pagination_class = MessagePagination

    def get_queryset(self):
        username = self.request.query_params.get("username")
        user = get_object_or_404(User, username=username)

        if user == self.request.user:
            raise Http404("user cannot send message to himself")

        queryset = Message.objects\
            .filter(sender=self.request.user,
                    receiver=user)\
            .order_by("sent_at")

        return queryset
