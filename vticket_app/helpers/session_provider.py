import json
from django.core.cache import cache
from rest_framework_simplejwt.tokens import AccessToken

class SessionProvider():
    __base_access_token_class = AccessToken

    def verify_token(self, token: str):
        try:
            user_id = self.__base_access_token_class(token=token).payload.get("user_id", None)
            return cache.has_key(f"session:{user_id}:access")
        except Exception as e:
            print(e)
            return False

    def get_context(self, token: str):
        try:
            user_id = self.__base_access_token_class(token=token).payload.get("user_id", None)
            session_data = json.loads(cache.get(f"session:{user_id}:access"))
            return session_data
        except Exception as e:
            print(e)
            return None
