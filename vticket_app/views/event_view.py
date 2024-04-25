from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from django.db import transaction, IntegrityError


from vticket_app.dtos.create_event_dto import CreateEventDto
from vticket_app.serializers.create_event_serializer import CreateEventSerializer
from vticket_app.services.event_service import EventService
from vticket_app.services.promotion_service import PromotionService
from vticket_app.utils.response import RestResponse
from vticket_app.decorators.validate_body import validate_body
from vticket_app.helpers.swagger_provider import SwaggerProvider
from vticket_app.middlewares.custom_permissions.is_business import IsBusiness

class EventView(viewsets.ViewSet):
    permission_classes = (IsBusiness,)
    event_service = EventService()
    promotion_service = PromotionService()

    @validate_body(CreateEventSerializer)
    @swagger_auto_schema(request_body=CreateEventSerializer, manual_parameters=[SwaggerProvider.header_authentication()])
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
    
    @action(methods=["GET"], detail=True, url_path="promotion", authentication_classes=(), permission_classes=())
    def get_promotions(self, request: Request, pk: str):
        try:
            result = self.promotion_service.get_promotions_by_event_id(int(pk))
            return RestResponse().success().set_data({"promotions": result}).response
        except Exception as e:
            print(e)
            return RestResponse().internal_server_error().response
        
    