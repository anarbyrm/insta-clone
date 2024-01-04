from django.urls import path

from accounts.api import views

urlpatterns = [
    path("profile", views.UserProfileView.as_view(), name="profile"),
    path("friend-request", views.FriendRequestView.as_view(), name="friend_request"),
]
