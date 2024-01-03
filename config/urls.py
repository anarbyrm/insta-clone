"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

API_VERSION = "v1"

urlpatterns_by_version = [
    path(f"api/{API_VERSION}/", include([
        path("", include("posts.urls")),
        path("", include("accounts.urls")),
    ]))
]

auth_urls = [
    path("auth/", include([
        path("", include("djoser.urls")),
        path("", include("djoser.urls.jwt")),
    ]))
]

urlpatterns = [
    path("admin/", admin.site.urls),
] + urlpatterns_by_version + auth_urls
