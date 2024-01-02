from django.urls import path
from rest_framework.routers import DefaultRouter

from posts.api import views

router = DefaultRouter()
router.register(r'posts', views.PostViewSet, basename='posts')
post_urls = router.urls

urlpatterns = post_urls + [
    
] 