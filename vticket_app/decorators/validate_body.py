from functools import wraps
from vticket_app.utils.response import RestResponse

def validate_body(validate_class):
    def callback_handler(callback):
        @wraps(callback)
        def wrapper(self, request, **kwargs):
            validate = validate_class(data=request.data)

            if not validate.is_valid():
                return RestResponse().validation_failed().set_data(validate.errors).response
            return callback(self, request, validate.validated_data, **kwargs)
        return wrapper
    return callback_handler