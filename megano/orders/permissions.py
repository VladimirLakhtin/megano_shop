from rest_framework import permissions


class IsOrderOwner(permissions.BasePermission):
    """Permission checking order owner"""

    def has_object_permission(self, request, view, obj) -> bool:
        return obj.profile == request.user.profile

