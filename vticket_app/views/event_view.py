from django.db import transaction, IntegrityError

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from drf_yasg.utils import swagger_auto_schema


from vticket_app.dtos.create_event_dto import CreateEventDto
from vticket_app.serializers.event_serializer import EventSerializer
from vticket_app.services.event_service import EventService
from vticket_app.utils.response import RestResponse
from vticket_app.decorators.validate_body import validate_body
from vticket_app.helpers.swagger_provider import SwaggerProvider
from vticket_app.middlewares.custom_permissions.is_business import IsBusiness

class EventView(viewsets.ViewSet):
    permission_classes = (IsBusiness,)
    event_service = EventService()

    @validate_body(EventSerializer)
    @swagger_auto_schema(request_body=EventSerializer, manual_parameters=[SwaggerProvider.header_authentication()])
    def create(self, request: Request, validated_body: dict):
        try:
            dto = CreateEventDto(**validated_body, owner_id=request.user.id)
            
            with transaction.atomic():
                is_success = self.event_service.create_event(dto)

                if not is_success:
                    raise IntegrityError()
            
            return RestResponse().success().response
        except IntegrityError:
            return RestResponse().defined_error().set_message("Chúng tôi không thể tạo sự kiện lúc này! Vui lòng thử lại sau ít phút.").response
        except Exception as e:
            print(e)
            return RestResponse().internal_server_error().response