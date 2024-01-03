from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from posts.models import Comment, Post
from posts.api.serializers import PostSerializer, PostUpdateSerializer, PostCommentSerializer
from posts.api.paginations import CustomizedPostPagination
from posts.api.permissions import IsOwner


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    lookup_field = "slug"
    pagination_class = CustomizedPostPagination
    permission_classes = (IsAuthenticated, IsOwner)

    def get_queryset(self):
        queryset = Post.objects\
            .select_related("user")\
            .filter(
                Q(is_public=True) |
                Q(user=self.request.user) |
                Q(user__in=self.request.user.user_profile.friends.all())
            )
        return queryset

    def get_serializer_class(self):
        if self.action in ("update", "partial_update"):
            return PostUpdateSerializer
        elif self.action == "comments":
            return PostCommentSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        current_user = self.request.user
        if self.action == "comments":
            post = self.get_object()
            return serializer.save(user=current_user, post=post)
        return serializer.save(user=current_user)

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

    @action(detail=True, url_path="comments", methods=["GET", "POST"])
    def comments(self, request, slug):
        post = self.get_object()
        serializer_class = self.get_serializer_class()

        if self.request.method == "POST":
            serializer = serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            data = {
                "data": serializer.data,
                "message": "Comment added to the post %s" % post.slug
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            post_comments = post.comments.all()
            serializer = serializer_class(post_comments, many=True)
            data = {
                "post": post.slug,
                "comments": serializer.data
            }
            return Response(data, status=status.HTTP_200_OK)


class CommentDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = PostCommentSerializer
    permission_classes = (IsAuthenticated, IsOwner)
