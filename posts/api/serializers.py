from rest_framework import serializers
from posts.models import Comment, Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            "id",
            "user",
            "file_type",
            "file",
            "description",
            "slug",
            "total_likes",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "user",
            "total_likes",
            "created_at",
            "updated_at",
        )


class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            "description",
            "slug",
        )
