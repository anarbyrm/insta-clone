from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class FileType(models.TextChoices):
    IMAGE = "IMAGE", "Image"
    VIDEO = "VIDEO", "Video"


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    file_type = models.CharField(max_length=10, choices=FileType.choices, default=FileType.IMAGE)
    file = models.FileField(upload_to="uploads")
    description = models.CharField(max_length=500, null=True, blank=True)
    slug = models.SlugField(max_length=100, unique=True)
    likes = models.ManyToManyField(User, blank=True, related_name="post_likes")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Post: {self.slug} ({self.user.username})"

    @property
    def total_likes(self):
        return self.likes.count()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField(max_length=500)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment: {self.user.username} on {self.post} at {self.created_at}"
