from django.urls import path

from accounts.api import views

urlpatterns = [
    path("profile", views.UserProfileView.as_view(), name="profile"),
]
