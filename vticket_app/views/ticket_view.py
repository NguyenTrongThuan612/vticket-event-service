import pytz
from datetime import datetime, timedelta
from django.core.cache import cache

from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.decorators import action

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from vticket_app.enums.calculate_bill_error_enum import CalculateBillErrorEnum
from vticket_app.enums.instance_error_enum import InstanceErrorEnum

from vticket_app.helpers.client_request_helper import get_client_ip
from vticket_app.helpers.swagger_provider import SwaggerProvider

from vticket_app.models.booking import Booking
from vticket_app.models.promotion import Promotion
from vticket_app.services.ticket_service import TicketService
from vticket_app.serializers.promotion_serializer import PromotionSerializer
from vticket_app.utils.response import RestResponse
from vticket_app.decorators.validate_body import validate_body
from vticket_app.middlewares.custom_permissions.is_customer import IsCustomer

from vticket_app.validations.booking_id_validator import BookingIdValidator
from vticket_app.validations.booking_validator import BookingValidator
from vticket_app.validations.pay_booking_validator import PayBookingValidator
from vticket_app.validations.update_booking_validator import UpdateBookingValidator

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
        
    @action(methods=["POST"], detail=False, url_path="booking/promotion", permission_classes=(IsCustomer, ))
    @swagger_auto_schema(request_body=BookingIdValidator, manual_parameters=[SwaggerProvider.header_authentication()])
    @validate_body(BookingIdValidator)
    def get_usable_promotions_by_booking(self, request: Request, validated_body: dict):
        try:
            bill_value, _, result = self.ticket_service.calculate_bill(validated_body["booking_id"])

            if result != CalculateBillErrorEnum.OK:
                return RestResponse().defined_error().set_data({"error": result.value}).response
            
            booking = Booking.objects.get(id=validated_body["booking_id"])
            
            promotions = self.ticket_service.get_usable_promotions_by_booking(booking.seats.all()[0].ticket_type.event, bill_value)

            return RestResponse().success().set_data(PromotionSerializer(promotions, many=True).data).response
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
        
    @action(methods=["POST"], detail=False, url_path="pay/preview")
    @swagger_auto_schema(manual_parameters=[SwaggerProvider.header_authentication()], request_body=PayBookingValidator)
    @validate_body(PayBookingValidator)
    def preview_pay_booking(self, request: Request, validated_body: dict):
        try:
            if not self.ticket_service.verify_booking_id(validated_body["booking_id"]):
                return RestResponse().defined_error().set_data("invalid_booking_id").response
            
            bill_value, calculate_detail, result = self.ticket_service.calculate_bill(
                validated_body["booking_id"], 
                validated_body["discount"]
            )

            if result != CalculateBillErrorEnum.OK:
                return RestResponse().defined_error().set_data({"error": result.value}).response
            
            return RestResponse().success().set_data(
                {
                    "bill_value": bill_value,
                    "calculate_detail": calculate_detail
                }
            ).response

        except Exception as e:
            print(e)
            return RestResponse().internal_server_error().response    
    
    @action(methods=["POST"], detail=False, url_path="pay")
    @swagger_auto_schema(manual_parameters=[SwaggerProvider.header_authentication()], request_body=PayBookingValidator)
    @validate_body(PayBookingValidator)
    def pay_booking(self, request: Request, validated_body: dict):
        try:
            pk = validated_body["booking_id"]

            if not self.ticket_service.verify_booking_id(pk):
                return RestResponse().defined_error().set_data({"error": "invalid_booking_id"}).response

            bill_value, _, result = self.ticket_service.calculate_bill(pk, validated_body["discount"])

            if result != CalculateBillErrorEnum.OK:
                return RestResponse().defined_error().set_data({"error": result.value}).response
            
            pay_url, ok = self.ticket_service.get_pay_url(
                pk,
                bill_value,
                get_client_ip(request),
                f"Thanh toan don hang {pk}",
                datetime.now(pytz.timezone("Asia/Ho_Chi_Minh")) + timedelta(minutes=10)
            )

            discount: Promotion = validated_body["discount"]

            if ok:
                if validated_body["discount"]:
                    cache.set(
                        f"booking:{pk}:discount:{discount.id}", 
                        discount.id, 
                        15*60
                    )
                return RestResponse().success().set_data({"url": pay_url}).response
            else:
                return RestResponse().defined_error().response
        except Exception as e:
            print(e)
            return RestResponse().internal_server_error().response
    
    @action(methods=["POST"], detail=False, url_path="update", authentication_classes=())
    @swagger_auto_schema(request_body=UpdateBookingValidator)
    @validate_body(UpdateBookingValidator)
    def update_booking(self, request: Request, validated_data: dict):
        try:
            ok = self.ticket_service.update_booking(
                payment_id=validated_data["payment_id"],
                booking_id=validated_data["booking_id"],
                paid_at=validated_data["paid_at"]
            )
            
            if ok:
                self.ticket_service.send_e_ticket(validated_data["payment_id"])
                return RestResponse().success().response
            else:
                return RestResponse().defined_error().response
        except Exception as e:
            print(e)
            return RestResponse().internal_server_error().response