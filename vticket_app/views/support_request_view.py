from rest_framework import viewsets
from rest_framework.request import Request
from drf_yasg.utils import swagger_auto_schema

from vticket_app.services.support_request_service import SupportRequestService
from vticket_app.serializers.support_request_serializer import SupportRequestSerializer
from vticket_app.dtos.create_support_request_dto import CreateSupportRequestDto
from vticket_app.middlewares.custom_permissions.is_customer import IsCustomer
from vticket_app.middlewares.custom_permissions.is_business import IsBusiness
from vticket_app.utils.response import RestResponse
from vticket_app.decorators.validate_body import validate_body
from vticket_app.helpers.swagger_provider import SwaggerProvider

class SupportRequestView(viewsets.ViewSet):
    support_request_service = SupportRequestService()
    permission_classes = (IsCustomer,)

    def get_permissions(self):
        return [IsBusiness()] if self.action in ["list"] else super().get_permissions()
    
    @validate_body(SupportRequestSerializer)
    @swagger_auto_schema(request_body=SupportRequestSerializer, manual_parameters=[SwaggerProvider.header_authentication()])
    def create(self, request: Request, validated_body: dict):
        try:
            dto = CreateSupportRequestDto(**validated_body, owner_id=request.user.id)
            is_created = self.support_request_service.create_request(dto)
            
            if is_created:
                return RestResponse().success().set_message("Gửi yêu cầu hỗ trợ thành công!").response    
            else:
                return RestResponse().defined_error().set_message("Xin lỗi, gửi yêu cầu hỗ trợ thất bại. Vui lòng xem xét lại dữ liệu đầu vào").response
        except Exception as e:
            print(e)
            return RestResponse().internal_server_error().response
    
    @swagger_auto_schema(manual_parameters=[SwaggerProvider.header_authentication()])
    def list(self, request: Request):
        try:
            data = self.support_request_service.get_all_request(request.user.id)

            return RestResponse().success().set_data(data).response
        except Exception as e:
            print(e)
            return RestResponse().internal_server_error().response  
        