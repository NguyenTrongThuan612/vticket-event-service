import json
from typing import Any
from django.core.cache import cache
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.settings import api_settings as jwt_configs

from vticket_app.enums.token_type import TokenTypeEnum

class SessionProvider():
    __base_access_token_class = AccessToken
    __prefix_key = "session"

    def verify_token(self, token: str):
        try:
            user_id = self.__base_access_token_class(token=token).payload.get("user_id", None)
            jti = self.__base_access_token_class(token=token).payload["jti"]
            return cache.has_key(f"{self.__prefix_key}:{user_id}:{TokenTypeEnum.access.value}:{jti}")
        except Exception as e:
            print(e)
            return False

    def get_context(self, token: str):
        try:
            token_payload = self.__base_access_token_class(token=token).payload
            user_id = token_payload.get("user_id", None)
            jti = token_payload.get("jti", None)
            session_data = json.loads(cache.get(f"{self.__prefix_key}:{user_id}:{TokenTypeEnum.access.value}:{jti}"))
            return session_data
        except Exception as e:
            print(e)
            return None
        
    def save_session(self, key: Any, data: Any, access_jti: str, refresh_jti: str):
        self.__remove_session(key, TokenTypeEnum.access)
        self.__remove_session(key, TokenTypeEnum.refresh)
        cache.set(f"{self.__prefix_key}:{str(key)}:{TokenTypeEnum.access.value}:{access_jti}", json.dumps(data), jwt_configs.ACCESS_TOKEN_LIFETIME.seconds)
        cache.set(f"{self.__prefix_key}:{str(key)}:{TokenTypeEnum.refresh.value}:{refresh_jti}", json.dumps(data), jwt_configs.ACCESS_TOKEN_LIFETIME.seconds)

    def __remove_session(self, key: Any, type: TokenTypeEnum):
        cache.delete_many(cache.keys(f"{self.__prefix_key}:{str(key)}:{type.value}:*"))