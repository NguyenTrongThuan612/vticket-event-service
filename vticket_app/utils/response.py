from rest_framework.response import Response

from vticket_app.enums.rest_response_status_enum import RestResponseStatusEnum

class RestResponse():
    content_type = "application/json"

    def __init__(self) -> None:
        self.__data = None
        self.__message = ""
        self.__status = 1
    
    def set_data(self, data: object):
        self.__data = data
        return self
    
    def set_message(self, message: str):
        self.__message = message
        return self
    
    def set_status(self, status: int):
        self.__status = status
        return self
    
    @property
    def response(self):
        return Response(
            {
                "data": self.__data,
                "status": self.__status,
                "message": self.__message,
            },
            content_type=self.content_type
        )
    
    def internal_server_error(self):
        self.__status = RestResponseStatusEnum.INTERNAL_SERVER_ERROR.value[0]
        self.__message = RestResponseStatusEnum.INTERNAL_SERVER_ERROR.value[1]
        return self
    
    def success(self):
        self.__status = RestResponseStatusEnum.SUCCESS.value[0]
        self.__message = RestResponseStatusEnum.SUCCESS.value[1]
        return self
    
    def permission_denied(self):
        self.__status = RestResponseStatusEnum.PERMISSION_DENIED.value[0]
        self.__message = RestResponseStatusEnum.PERMISSION_DENIED.value[1]
        return self
    
    def throttled(self):
        self.__status = RestResponseStatusEnum.THROTTLED.value[0]
        self.__message = RestResponseStatusEnum.THROTTLED.value[1]
        return self
    
    def validation_failed(self):
        self.__status = RestResponseStatusEnum.VALIDATION_FAILED.value[0]
        self.__message = RestResponseStatusEnum.VALIDATION_FAILED.value[1]
        return self
    
    def defined_error(self):
        self.__status = RestResponseStatusEnum.DEFINED_ERROR.value[0]
        self.__message = RestResponseStatusEnum.DEFINED_ERROR.value[1]
        return self
    
    def direct(self, to: str):
        self.__data = {
            "target": to
        }
        self.__status = RestResponseStatusEnum.DIRECT.value[0]
        self.__message = RestResponseStatusEnum.DIRECT.value[1]
        return self