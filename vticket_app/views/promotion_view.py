from rest_framework import viewsets
from rest_framework.request import Request
from drf_yasg.utils import swagger_auto_schema
from django.db import transaction, IntegrityError

from vticket_app.dtos.create_promotion_dto import CreatePromotionDto
from vticket_app.enums.instance_error_enum import InstanceErrorEnum
from vticket_app.helpers.swagger_provider import SwaggerProvider
from vticket_app.middlewares.custom_permissions.is_business import IsBusiness
from vticket_app.utils.response import RestResponse
from vticket_app.decorators.validate_body import validate_body
from vticket_app.services.promotion_service import PromotionService
from vticket_app.serializers.create_promotion_serializer import CreatePromotionSerializer
from vticket_app.serializers.promotion_serializer import PromotionSerializer

class PromotionView(viewsets.ViewSet):
    promotion_service = PromotionService()

    @swagger_auto_schema(request_body=CreatePromotionSerializer, manual_parameters=[SwaggerProvider().header_authentication()])
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
    
    @swagger_auto_schema(manual_parameters=[SwaggerProvider().header_authentication()])
    def destroy(self, request: Request, pk: int):
        try:
            result = self.promotion_service.delete_promotion(int(pk))
            return {
                InstanceErrorEnum.ALL_OK: RestResponse().success().set_message("Xóa khuyến mãi thành công!").response,
                InstanceErrorEnum.DELETED: RestResponse().defined_error().set_message("Khuyến mãi này đã bị xóa rồi!").response,
                InstanceErrorEnum.NOT_EXISTED: RestResponse().defined_error().set_message("Khuyến mãi không tồn tại!").response
            }[result]
        except Exception as e:
            print(e)
            return RestResponse().internal_server_error().response