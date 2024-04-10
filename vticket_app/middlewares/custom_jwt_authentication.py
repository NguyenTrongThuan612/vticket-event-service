from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from vticket_app.dtos.user_dto import UserDTO
from vticket_app.helpers.session_provider import SessionProvider

class CustomJWTAuthentication(BaseAuthentication):
    session_provider = SessionProvider()

    def authenticate(self, request):
        bearer_token = request.headers.get("Authorization", None)

        if bearer_token is None:
            raise AuthenticationFailed("Missing token!")
        
        token = bearer_token.replace("Bearer ", "")

        if not self.session_provider.verify_token(token=token):
            raise AuthenticationFailed("Verify token failed!")
        
        session_data = self.session_provider.get_context(token=token)
        user_dto = UserDTO(**session_data)
        
        return (user_dto, None)