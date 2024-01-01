from django.urls import path
from posts.api import views

urlpatterns = [
    path('posts', views.PostListView.as_view(), name="post_list_create"),
    path('posts/<slug:slug>', views.PostDetailView.as_view(), name="post_detail"),
    # path('posts/<slug:post_slug>/comments', views, name="post_comments"),
    # path('comments/<int:comment_id>', views, name="post_comments"),
]