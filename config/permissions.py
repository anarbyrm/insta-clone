from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        EDIT_METHODS = ("PUT", "PATCH", "DELETE")

        if request.user.is_superuser or request.method not in EDIT_METHODS:
            return True

        return obj.user == request.user
