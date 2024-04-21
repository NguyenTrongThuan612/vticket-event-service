from rest_framework import viewsets
from rest_framework.request import Request
from drf_yasg.utils import swagger_auto_schema
from django.db import IntegrityError

from vticket_app.dtos.create_support_response_dto import CreateSupportResponseDto
from vticket_app.serializers.support_response_serializer import SupportResponseSerializer
from vticket_app.services.support_response_service import SupportResponseService
from vticket_app.middlewares.custom_permissions.is_business import IsBusiness
from vticket_app.middlewares.custom_permissions.is_onwer import IsOwner
from vticket_app.utils.response import RestResponse
from vticket_app.decorators.validate_body import validate_body
from vticket_app.helpers.swagger_provider import SwaggerProvider

class SupportResponseView(viewsets.ViewSet):
    support_response_service = SupportResponseService()
    permission_classes = (IsBusiness, IsOwner)
    
    @validate_body(SupportResponseSerializer)
    @swagger_auto_schema(request_body=SupportResponseSerializer, manual_parameters=[SwaggerProvider.header_authentication()])
    def create(self, request: Request, validated_body: dict):
        try:
            dto = CreateSupportResponseDto(**validated_body, owner_id=request.user.id)
            created = self.support_response_service.create_response(dto)
            if not created:
                raise IntegrityError()
            return RestResponse().success().set_message("Phản hồi hỗ trợ thành công!").response    
        except IntegrityError:
            return RestResponse().defined_error().set_message("Xin lỗi, gửi phản hồi hỗ trợ thất bại. Vui lòng xem xét lại dữ liệu đầu vào").response
        except Exception as e:
            print(e)
            return RestResponse().internal_server_error().response
    
    @swagger_auto_schema(manual_parameters=[SwaggerProvider.header_authentication()])
    def list(self, request: Request):
        try:
            data = self.support_response_service.get_all_response(request.user.id)
            return RestResponse().success().set_data(data).response
        except Exception as e:
            print(e)
            return RestResponse().internal_server_error().response  