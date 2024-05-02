from rest_framework import viewsets
from rest_framework.request import Request
from drf_yasg.utils import swagger_auto_schema

from vticket_app.services.feedback_service import FeedbackService
from vticket_app.serializers.feedback_serializer import FeedbackSerializer
from vticket_app.dtos.create_feedback_dto import CreateFeedbackDto
from vticket_app.middlewares.custom_permissions.is_customer import IsCustomer
from vticket_app.utils.response import RestResponse
from vticket_app.decorators.validate_body import validate_body
from vticket_app.helpers.swagger_provider import SwaggerProvider

class FeedbackView(viewsets.ViewSet):
    feedback_service = FeedbackService()
    permission_classes = (IsCustomer, )
    
    @validate_body(FeedbackSerializer)
    @swagger_auto_schema(request_body=FeedbackSerializer, manual_parameters=[SwaggerProvider.header_authentication()])
    def create(self, request: Request, validated_body: dict):
        try:
            dto = CreateFeedbackDto(**validated_body, owner_id=request.user.id)
            is_created = self.feedback_service.create_feedback(dto)
            
            if is_created:
                return RestResponse().success().set_message("Gửi nhận xét thành công!").response    
            else:
                return RestResponse().defined_error().set_message("Xin lỗi, gửi nhận xét thất bại. Vui lòng xem xét lại dữ liệu đầu vào").response
        except Exception as e:
            print(e)
            return RestResponse().internal_server_error().response
        
    @swagger_auto_schema(manual_parameters=[SwaggerProvider.header_authentication()])
    def list(self, request: Request):
        try:
            data = self.feedback_service.get_all_feedback(request.user.id)

            return RestResponse().success().set_data(data).response
        except Exception as e:
            print(e)
            return RestResponse().internal_server_error().response  