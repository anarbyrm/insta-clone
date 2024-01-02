from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from posts.models import Comment, Post
from posts.api.serializers import PostSerializer, PostUpdateSerializer


"""
Replaced with viewset
"""
# class PostListView(ListCreateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

#     def get_queryset(self):
#         queryset = Post.objects\
#             .select_related("user").all()
#             #.filter(Q(user=self.request.user)) # TODO: implement seeing only owned and friends posts
#         return queryset
    
#     def perform_create(self, serializer):
#         return serializer.save(user=self.request.user)


# class PostDetailView(RetrieveUpdateDestroyAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     lookup_field = "slug"

#     def get_serializer_class(self):
#         if self.request.method in ("PUT", "PATCH"):
#             return PostUpdateSerializer
#         return self.serializer_class


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    lookup_field = "slug"
    # authentication_classes = ()
    # permission_classes = ()

    def get_queryset(self):
        queryset = Post.objects\
            .select_related("user").all()
            #.filter(Q(user=self.request.user)) # TODO: implement seeing only owned and friends posts
        return queryset

    def get_serializer_class(self):
        if self.action in ("update", "partial_update"):
            return PostUpdateSerializer
        return self.serializer_class
    
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    @action(detail=True, url_path="like", methods=["POST"])
    def like(self, request, slug):
        post = self.get_object()
        current_user = request.user
        if current_user not in post.likes.all():
            post.likes.add(current_user)
            return Response({"message": "You liked the post: %s" % post.slug},
                        status=status.HTTP_200_OK)
        return Response({"message": "You already liked the post: %s" % post.slug},
                        status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, url_path="unlike", methods=["POST"])
    def unlike(self, request, slug):
        post = self.get_object()
        current_user = request.user
        if current_user in post.likes.all():
            post.likes.remove(current_user)
            return Response({"message": "You removed the like from the post: %s" % post.slug},
                        status=status.HTTP_200_OK)
        return Response({"message": "You already unliked the post: %s" % post.slug},
                        status=status.HTTP_400_BAD_REQUEST)

