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
            "is_public",
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
            "user",
            "file_type",
            "file",
            "slug",
            "likes",
            "is_public",
            "created_at",
            "updated_at",
            "description",
        )
        read_only_fields = (
            "user",
            "file_type",
            "file",
            "slug",
            "likes",
            "created_at",
            "updated_at",
        )


class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            "id",
            "user",
            "post",
            "text",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "user",
            "post",
            "created_at",
            "updated_at",
        )
