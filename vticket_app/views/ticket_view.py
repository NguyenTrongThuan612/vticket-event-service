from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from django.db import transaction, IntegrityError
from drf_yasg import openapi

from vticket_app.enums.instance_error_enum import InstanceErrorEnum
from vticket_app.utils.response import RestResponse
from vticket_app.services.ticket_service import TicketService
from vticket_app.decorators.validate_body import validate_body
from vticket_app.helpers.swagger_provider import SwaggerProvider
from vticket_app.middlewares.custom_permissions.is_customer import IsCustomer
from vticket_app.validations.booking_validator import BookingValidator

class TicketView(viewsets.ViewSet):
    ticket_service = TicketService()

    @validate_body(BookingValidator)
    @action(methods=["POST"], detail=False, url_path="booking", permission_classes=(IsCustomer, ))
    @swagger_auto_schema(request_body=BookingValidator, manual_parameters=[SwaggerProvider.header_authentication()])
    def booking(self, request: Request, validated_body: dict):
        try:
            result, id = self.ticket_service.booking(request.user.id, validated_body["seats"])

            return {
                InstanceErrorEnum.ALL_OK: RestResponse().success().set_data({"booking_id": id}).response,
                InstanceErrorEnum.EXCEPTION: RestResponse().defined_error().set_message("Đặt vé thất bại! Vui lòng thử lại sau ít phút!").response,
                InstanceErrorEnum.EXISTED: RestResponse().defined_error().set_message("Rất tiếc! Ghế bạn chọn không còn trống!").response
            }[result]

        except Exception as e:
            print(e)
            return RestResponse().internal_server_error().response
        
    @action(methods=["GET"], detail=False, url_path="filter", permission_classes=(IsCustomer, ))
    @swagger_auto_schema(manual_parameters=[
        SwaggerProvider.header_authentication(),
        SwaggerProvider.query_param("filter", openapi.TYPE_STRING)
        ]
    )
    def list_tickets(self, request: Request):
        try:
            filter = request.query_params.get("filter", None)
            data = self.ticket_service.list_tickets(request.user.id, filter)
            return RestResponse().success().set_data(data).response
        except Exception as e:
            print(e)
            return RestResponse().internal_server_error().response

        
    