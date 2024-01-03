from django.urls import path

from accounts.api import views

urlpatterns = [
    path("profile", views.ProfileView.as_view(), name="profile"),
]
