from rest_framework import viewsets
from rest_framework.request import Request
from drf_yasg.utils import swagger_auto_schema

from vticket_app.services.feedback_service import FeedbackService
from vticket_app.dtos.create_feedback_reply_dto import CreateFeedbackReplyDto
from vticket_app.serializers.feedback_reply_serializer import FeedbackReplySerializer
from vticket_app.services.feedback_reply_service import FeedbackReplyService
from vticket_app.middlewares.custom_permissions.is_business import IsBusiness
from vticket_app.utils.response import RestResponse
from vticket_app.decorators.validate_body import validate_body
from vticket_app.helpers.swagger_provider import SwaggerProvider

class FeedbackReplyView(viewsets.ViewSet):
    feedback_service = FeedbackService()
    feedback_reply_service = FeedbackReplyService()
    permission_classes = (IsBusiness,)
    
    @validate_body(FeedbackReplySerializer)
    @swagger_auto_schema(request_body=FeedbackReplySerializer, manual_parameters=[SwaggerProvider.header_authentication()])
    def create(self, request: Request, validated_body: dict):
        try:
            feedback = self.feedback_service.get_feedback_by_id(feedback_id=validated_body["feedback"].id)
            if feedback is None:
                return RestResponse().defined_error().set_message("Đánh giá không tồn tại!").response
            
            if not self.feedback_service.can_reply(feedback, request.user):
                return RestResponse().permission_denied().set_message("Bạn không có quyền trả lời đánh giá này!").response
            
            dto = CreateFeedbackReplyDto(**validated_body, owner_id=request.user.id)
            is_created = self.feedback_reply_service.create_reply(dto)

            if is_created:
                return RestResponse().success().set_message("Trả lời đánh giá thành công!").response    
            else:
                return RestResponse().defined_error().set_message("Đã xảy ra chút sự cố! Bạn vui lòng chờ đợi trong khi chúng tôi nỗ lực khắc phục vấn đề!").response
        except Exception as e:
            print(e)
            return RestResponse().internal_server_error().response