from rest_framework import viewsets
from rest_framework.request import Request
from drf_yasg.utils import swagger_auto_schema
from django.db import transaction, IntegrityError

from vticket_app.dtos.create_event_dto import CreateEventDto
from vticket_app.serializers.event_serializer import EventSerializer
from vticket_app.utils.response import RestResponse
from vticket_app.serializers.create_event_serializer import CreateEventSerializer
from vticket_app.decorators.validate_body import validate_body

from vticket_app.services.event_service import EventService
from vticket_app.services.promotion_service import PromotionService

from vticket_app.helpers.swagger_provider import SwaggerProvider
from vticket_app.helpers.image_storage_providers.image_storage_provider import ImageStorageProvider
from vticket_app.helpers.image_storage_providers.firebase_storage_provider import FirebaseStorageProvider

from vticket_app.middlewares.custom_permissions.is_business import IsBusiness

class EventManagementView(viewsets.ViewSet):
    image_storage_provider: ImageStorageProvider = FirebaseStorageProvider()
    event_service = EventService()
    promotion_service = PromotionService()
    permission_classes = (IsBusiness, )

    @validate_body(CreateEventSerializer)
    @swagger_auto_schema(request_body=CreateEventSerializer, manual_parameters=[SwaggerProvider.header_authentication()])
    def create(self, request: Request, validated_body: dict):
        try:
            dto = CreateEventDto(**validated_body, owner_id=request.user.id)
            
            with transaction.atomic():
                instance = self.event_service.create_event(dto)

                if instance is None:
                    raise IntegrityError()

            self.event_service.send_new_event_email(instance)
            
            return RestResponse().success().response
        except IntegrityError:
            return RestResponse().defined_error().set_message("Chúng tôi không thể tạo sự kiện lúc này! Vui lòng thử lại sau ít phút.").response
        except Exception as e:
            print(e)
            return RestResponse().internal_server_error().response
        

    @swagger_auto_schema(manual_parameters=[SwaggerProvider.header_authentication()])
    def list(self, request: Request):
        try:
            events = self.event_service.get_all_event(request.user.id)

            return RestResponse().success().set_data({"event": EventSerializer(events, many=True, exclude=["ticket_types"]).data}).response
        except Exception as e:
            print(e) 
            return RestResponse().internal_server_error().response
