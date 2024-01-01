from django.db.models import Q
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from posts.models import Comment, Post
from posts.api.serializers import PostSerializer, PostUpdateSerializer


class PostListView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        queryset = Post.objects\
            .select_related("user").all()
            #.filter(Q(user=self.request.user)) # TODO: implement seeing only owned and friends posts
        return queryset
    
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class PostDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return PostUpdateSerializer
        return self.serializer_class
