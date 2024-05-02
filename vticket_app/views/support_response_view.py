from rest_framework import viewsets
from rest_framework.request import Request
from drf_yasg.utils import swagger_auto_schema
from django.db import IntegrityError

from vticket_app.services.support_request_service import SupportRequestService
from vticket_app.dtos.create_support_response_dto import CreateSupportResponseDto
from vticket_app.serializers.support_response_serializer import SupportResponseSerializer
from vticket_app.services.support_response_service import SupportResponseService
from vticket_app.middlewares.custom_permissions.is_business import IsBusiness
from vticket_app.utils.response import RestResponse
from vticket_app.decorators.validate_body import validate_body
from vticket_app.helpers.swagger_provider import SwaggerProvider

class SupportResponseView(viewsets.ViewSet):
    support_response_service = SupportResponseService()
    support_request_service = SupportRequestService()
    permission_classes = (IsBusiness,)
    
    @validate_body(SupportResponseSerializer)
    @swagger_auto_schema(request_body=SupportResponseSerializer, manual_parameters=[SwaggerProvider.header_authentication()])
    def create(self, request: Request, validated_body: dict):
        try:
            support_request = self.support_request_service.get_request_by_id(request_id=validated_body["request"].id)
            if support_request is None:
                return RestResponse().defined_error().set_message("Yêu cầu hỗ trợ không tồn tại!").response
            
            if not self.support_request_service.can_reply(support_request, request.user):
                return RestResponse().permission_denied().set_message("Bạn không có quyền phản hồi hỗ trợ này!").response
            
            dto = CreateSupportResponseDto(**validated_body, owner_id=request.user.id)
            is_created = self.support_response_service.create_response(dto)

            if is_created:
                return RestResponse().success().set_message("Phản hồi hỗ trợ thành công!").response    
            else:
                return RestResponse().defined_error().set_message("Đã xảy ra chút sự cố! Bạn vui lòng chờ đợi trong khi chúng tôi nỗ lực khắc phục vấn đề!").response
        except Exception as e:
            print(e)
            return RestResponse().internal_server_error().response