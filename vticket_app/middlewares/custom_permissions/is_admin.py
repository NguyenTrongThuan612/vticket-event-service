from rest_framework import permissions

from vticket_app.enums.role_enum import RoleEnum

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == RoleEnum.ADMIN