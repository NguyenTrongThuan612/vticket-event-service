from rest_framework.views import exception_handler

from vticket_app.utils.response import RestResponse

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    return {
        403: RestResponse().invalid_token().response,
    }.get(response.status_code, response)