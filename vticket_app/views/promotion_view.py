from rest_framework import viewsets
from rest_framework.request import Request
from drf_yasg.utils import swagger_auto_schema
from django.db import transaction, IntegrityError

from vticket_app.dtos.create_promotion_dto import CreatePromotionDto
from vticket_app.utils.response import RestResponse
from vticket_app.decorators.validate_body import validate_body
from vticket_app.services.promotion_service import PromotionService
from vticket_app.serializers.create_promotion_serializer import CreatePromotionSerializer

class PromotionView(viewsets.ViewSet):
    promotion_service = PromotionService()
    authentication_classes = ()

    @swagger_auto_schema(request_body=CreatePromotionSerializer)
    @validate_body(CreatePromotionSerializer)
    def create(self, request: Request, validated_body: dict):
        try:
            dto = CreatePromotionDto(**validated_body)

            with transaction.atomic():
                is_created = self.promotion_service.create_promotion(dto)

                if not is_created:
                    raise IntegrityError("Transaction failed!")
            
            return RestResponse().success().set_message("Tạo khuyến mãi thành công!").response
        except IntegrityError as e:
            return RestResponse().defined_error().set_message("Đã xảy ra lỗi trong quá trình tạo khuyến mãi!").response
        except Exception as e:
            print(e)
            return RestResponse().internal_server_error().response