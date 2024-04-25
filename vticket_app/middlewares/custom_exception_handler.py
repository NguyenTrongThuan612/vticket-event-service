from typing import Union

from rest_framework import exceptions
from rest_framework.views import exception_handler

from vticket_app.utils.response import RestResponse

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    print(response, exc)
    return {
        401: RestResponse().invalid_token().response,
        403: RestResponse().permission_denied().response
    }.get(exc_to_status(exc_class=exc.__class__) or response.status_code, response)

def exc_to_status(exc_class) -> Union[int, None]:
    return {
        exceptions.AuthenticationFailed: 401,
        exceptions.NotAuthenticated: 401
    }.get(exc_class, None)