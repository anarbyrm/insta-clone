from django.contrib import admin

from accounts.models import FriendshipRequest, Profile

admin.site.register(Profile)
admin.site.register(FriendshipRequest)
