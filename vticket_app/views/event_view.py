from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db import transaction, IntegrityError


from vticket_app.dtos.create_event_dto import CreateEventDto
from vticket_app.helpers.image_storage_providers.image_storage_provider import ImageStorageProvider
from vticket_app.helpers.image_storage_providers.firebase_storage_provider import FirebaseStorageProvider
from vticket_app.serializers.create_event_serializer import CreateEventSerializer
from vticket_app.services.event_service import EventService
from vticket_app.services.promotion_service import PromotionService
from vticket_app.utils.response import RestResponse
from vticket_app.decorators.validate_body import validate_body
from vticket_app.helpers.swagger_provider import SwaggerProvider
from vticket_app.middlewares.custom_permissions.is_business import IsBusiness
from vticket_app.middlewares.custom_permissions.is_customer import IsCustomer
from vticket_app.validations.change_banner_validator import ChangeBannerValidator

class EventView(viewsets.ViewSet):
    permission_classes = (IsBusiness,)
    image_storage_provider: ImageStorageProvider = FirebaseStorageProvider()
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
        
    @action(methods=["GET"], detail=False, url_path="search", permission_classes=(IsCustomer,))
    @swagger_auto_schema(manual_parameters=[
        SwaggerProvider.header_authentication(),
        SwaggerProvider.query_param("kw", openapi.TYPE_STRING)
        ]
    )
    def search(self, request: Request):
        try:
            keyword = request.query_params.get("kw", None) 
            data = self.event_service.search_event(keyword=keyword)
            return RestResponse().success().set_data(data).response
        except Exception as e:
            print(e)
            return RestResponse().internal_server_error().response
        
    @action(methods=["GET"], detail=False, url_path="value-types",authentication_classes=(), permission_classes=())
    def get_value_types(self, request: Request):
        try:
            ticket_types = self.event_service.get_value_types_enum()
            return RestResponse().success().set_data({"ticket_types": ticket_types}).response
        except Exception as e:
            print(e)
            return RestResponse().internal_server_error().response
        
    @action(methods=["POST"], detail=False, url_path="banner", parser_classes=[MultiPartParser])
    @swagger_auto_schema(
        request_body=None,
        manual_parameters=[
            SwaggerProvider.header_authentication(),
            SwaggerProvider.form_data("image", openapi.TYPE_FILE)
        ]
    )
    @validate_body(ChangeBannerValidator)
    def change_banner(self, request: Request, validated_body):
        try:
            url = self.image_storage_provider.upload_image(validated_body["image"])
            updated = self.event_service.change_banner(validated_body["event"].id, url)
            if updated:
                return RestResponse().success().set_data({"banner_url": url}).set_message("Một diện mạo mới, một tinh thần mới! 😄✨").response
            else:
                return RestResponse().defined_error().set_message("Có chút trục trặc trong khi chúng tôi đang cố gắng thay bức hình tuyệt vời này!").response
        except Exception as e:
            print(e)
            return RestResponse().internal_server_error().response