from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema

from vticket_app.helpers.swagger_provider import SwaggerProvider
from vticket_app.middlewares.custom_permissions.is_admin import IsAdmin
from vticket_app.serializers.event_serializer import EventSerializer
from vticket_app.services.event_service import EventService
from vticket_app.utils.response import RestResponse
from vticket_app.decorators.validate_body import validate_body
from vticket_app.services.event_topic_service import EventTopicService
from vticket_app.serializers.event_topic_serializer import EventTopicSerializer
from vticket_app.validations.event_topic_validator import EventTopicValidator

class EventTopicView(viewsets.ViewSet):
    event_topic_service = EventTopicService()
    permission_classes = [IsAdmin]
    event_service = EventService()

    def get_permissions(self):
        return [] if self.action in ["list"] else super().get_permissions()
    
    @action(methods=["GET"], detail=True, url_path="events", permission_classes=(), authentication_classes=())
    def get_events_by_topic(self, request: Request, pk: int):
        try:
            validate = EventTopicValidator(data={"event_topic": pk})

            if not validate.is_valid():
                return RestResponse().validation_failed().set_data(validate.errors).response
            
            events = self.event_service.get_events_by_topic(validate.validated_data["event_topic"])
            
            return RestResponse().success().set_data(EventSerializer(events, many=True, exclude=["ticket_types"]).data).response
        except Exception as e:
            print(e)
            return RestResponse().internal_server_error().response

    @validate_body(EventTopicSerializer)
    @swagger_auto_schema(request_body=EventTopicSerializer, manual_parameters=[SwaggerProvider.header_authentication()])
    def create(self, request: Request, validated_body: dict):
        try:
            created = self.event_topic_service.create_topic(name=validated_body["name"], description=validated_body["description"])

            if created:
                return RestResponse().success().set_message("Tuyệt vời! Bạn đã đặt nền móng cho một sự kiện thú vị!").response
            else:
                return RestResponse().defined_error().set_message("Xin lỗi, không thể tạo chủ đề sự kiện. Vui lòng thử lại sau hoặc liên hệ với quản trị viên để biết thêm chi tiết.").response
        except Exception as e:
            print(e)
            return RestResponse().internal_server_error().response
    
    @swagger_auto_schema(manual_parameters=[SwaggerProvider.header_authentication()])
    def list(self, request: Request):
        try:
            data = self.event_topic_service.get_all_topics()
            return RestResponse().success().set_data(data).response
        except Exception as e:
            print(e)
            return RestResponse().internal_server_error().response
        
    @swagger_auto_schema(manual_parameters=[SwaggerProvider.header_authentication()])
    def destroy(self, request, pk):
        try:
            deleted = self.event_topic_service.delete_topic(pk)

            if deleted:
                return RestResponse().success().set_message("Thành công!").response
            else:
                return RestResponse().defined_error().set_message("Chủ đề không tồn tại hoặc đã bị xóa!").response
        except Exception as e:
            print(e)
            return RestResponse().internal_server_error().response