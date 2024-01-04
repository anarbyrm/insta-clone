from django.urls import path

from accounts.api import views

urlpatterns = [
    path("profile", views.UserProfileView.as_view(), name="profile"),
    path("friendship/requests", views.FriendRequestView.as_view(), name="friend_requests"),
    path("friendship/response/<str:pk>", views.FriendRequestResponseView.as_view(), name="friend_response"),
]
