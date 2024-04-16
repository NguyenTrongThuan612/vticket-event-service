from rest_framework import permissions

from vticket_app.enums.role_enum import RoleEnum

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner_id == request.user.user_id