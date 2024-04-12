from rest_framework import permissions

from vticket_app.enums.role_enum import RoleEnum

class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == RoleEnum.CUSTOMER