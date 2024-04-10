from rest_framework.permissions import BasePermission

from vticket_app.helpers.session_provider import SessionProvider

class IsAuthenticated(BasePermission):
    session_provider = SessionProvider()

    def has_permission(self, request, view):
        print(request.headers)
        return True