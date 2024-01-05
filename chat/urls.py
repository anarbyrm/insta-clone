from django.urls import path

from rest_framework.routers import DefaultRouter

from chat.api import views

router = DefaultRouter()
router.register("messages", views.MessageViewSet, basename="message")
message_urls = router.urls


urlpatterns = message_urls + [
   # additional pathes here 
]
