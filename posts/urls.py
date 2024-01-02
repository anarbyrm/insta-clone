from django.urls import path
from rest_framework.routers import DefaultRouter

from posts.api import views

router = DefaultRouter()
router.register(r'posts', views.PostViewSet, basename='posts')
post_urls = router.urls

urlpatterns = post_urls + [
    # replaced with router
    # path('posts', views.PostListView.as_view(), name="post_list_create"),
    # path('posts/<slug:slug>', views.PostDetailView.as_view(), name="post_detail"),

    # path('posts/<slug:post_slug>/comments', views, name="post_comments"),
    # path('comments/<int:comment_id>', views, name="post_comments"),
] 