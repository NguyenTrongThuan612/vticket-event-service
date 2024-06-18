import json
import pytz
import requests
import datetime
import dataclasses
from uuid import uuid4
from typing import Tuple, Union

from django.utils import timezone
from django.db import transaction
from django.db.models import Q, Case, When, Value, BooleanField, Sum, F
from django.core.cache import cache

from vticket_app.configs.related_services import RelatedService
from vticket_app.enums.calculate_bill_error_enum import CalculateBillErrorEnum
from vticket_app.enums.discount_type_enum import DiscountTypeEnum
from vticket_app.enums.fee_type_enum import FeeTypeEnum
from vticket_app.enums.promotion_evaluation_condition_enum import PromotionEvaluationConditionEnum
from vticket_app.models.event import Event
from vticket_app.models.promotion import Promotion
from vticket_app.models.ticket_type import TicketType
from vticket_app.models.ticket_type_detail import TicketTypeDetail
from vticket_app.models.seat_configuration import SeatConfiguration
from vticket_app.models.user_ticket import UserTicket
from vticket_app.models.booking import Booking

from vticket_app.dtos.ticket_type_dto import TicketTypeDto
from vticket_app.dtos.ticket_type_detail_dto import TicketTypeDetailDto
from vticket_app.dtos.seat_configuration_dto import SeatConfigurationDto

from vticket_app.enums.instance_error_enum import InstanceErrorEnum
from vticket_app.serializers.user_ticket_serializer import UserTicketSerializer

class TicketService():
    booking_payment_minute = 15

    def create_ticket_types(self, dataset: list[TicketTypeDto], event: Event) -> bool:
        try:
            for data in dataset:
                _details = data.ticket_type_details
                _seats = data.seat_configurations
                
                _data = dataclasses.asdict(data)
                _data.pop("ticket_type_details")
                _data.pop("seat_configurations")

                instance = TicketType.objects.create(event=event, **_data)
                result = (
                    bool(instance.id)
                    and self.config_seats(_seats, instance)
                    and self.create_ticket_type_details(_details, instance)
                )
                
                if not result:
                    return False
                
            return True
        except Exception as e:
            print(e)
            return False
        
    def create_ticket_type_details(self, dataset: list[TicketTypeDetailDto], ticket_type: TicketType):
        try:
            instances = TicketTypeDetail.objects.bulk_create(
                [
                    TicketTypeDetail(
                        ticket_type=ticket_type, 
                        **dataclasses.asdict(data)
                    ) 
                    for data in dataset
                ]
            )
            return all(bool(instance.id) for instance in instances)
        except Exception as e:
            print(e)
            return False
        
    def config_seats(self, dataset: list[SeatConfigurationDto], ticket_type: TicketType) -> bool:
        try:
            instances = []

            for data in dataset:
                for seat_number in range(data.start_seat_number, data.end_seat_number):
                    instances.append(
                        SeatConfiguration(
                            ticket_type=ticket_type,
                            position=data.position,
                            seat_number=seat_number
                        )
                    )
            SeatConfiguration.objects.bulk_create(instances)
            
            return all(bool(instance.id) for instance in instances)
        except Exception as e:
            print(e)
            return False
        
    def booking(self, user_id: int, seats: list[SeatConfiguration]) -> Union[InstanceErrorEnum, Tuple[str, None]]:
        try:
            for seat in seats:
                if cache.keys(f"booking:*:seat:{seat.id}") or seat.user_tickets.filter(is_refunded=False).exists():
                    return InstanceErrorEnum.EXISTED, None
            
            _booking_id = uuid4().hex

            self._cache_booking(_booking_id, user_id, seats)
            self._save_booking(_booking_id, user_id, seats)

            return InstanceErrorEnum.ALL_OK, _booking_id
        except Exception as e:
            print(e)
            return InstanceErrorEnum.EXCEPTION, None
        
    def _cache_booking(self, id: str, user_id: int, seats: list[SeatConfiguration]):
        _booking_data = {}

        for seat in seats:
            _booking_data[f"booking:{id}:seat:{seat.id}"] = {
                "user_id": user_id,
                "seat_id": seat.id
            }
        
        cache.set_many(_booking_data, self.booking_payment_minute*60)

    def _save_booking(self, id: str, user_id: int, seats: list[SeatConfiguration]):
        try:
            with transaction.atomic():
                instance = Booking(id=id, user_id=user_id)
                instance.save()
                instance.seats.set(seats)
        except Exception as e:
            print(e)

    def filter_ticket(self, field: str, queryset: list[TicketType]) -> list[TicketType]:
        if field == 'created_at':
            queryset = queryset.order_by('seat__ticket_type__event__created_at')
        elif field == 'event_start_time':
            current_datetime = timezone.now()
            current_date = current_datetime.date()
            current_time = current_datetime.time()
            queryset = queryset.annotate(
                has_started=Case(
                When(Q(seat__ticket_type__event__start_date__gt=current_date) |
                     (Q(seat__ticket_type__event__start_date=current_date) &
                      Q(seat__ticket_type__event__start_time__gt=current_time)), then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
                )
            ).order_by("-has_started",'seat__ticket_type__event__start_date', 'seat__ticket_type__event__start_time')
        return queryset
        
    def list_tickets(self, user_id: int, order_by: str) -> list[TicketType]:
        queryset = UserTicket.objects.filter(user_id=user_id)

        if order_by is not None:
            queryset = self.filter_ticket(order_by, queryset)
            
        return UserTicketSerializer(
            queryset, 
            many=True, 
            exclude=["user_id"], 
            context={
                "user_id": user_id
            }
        ).data
    
    def get_pay_url(self, order_id: str, amount: int, customer_ip: str, order_info: str, expire_date: datetime.datetime) -> Tuple[str, bool]:
        try:
            resp = requests.post(
                url=f"{RelatedService.payment}/payment/pay-url",
                data=json.dumps(
                    {
                        "order_id": order_id,
                        "amount": amount,
                        "created_date": datetime.datetime.now(pytz.timezone("Asia/Ho_Chi_Minh")).strftime("%Y-%m-%d:%H:%M:%S"),
                        "customer_ip": customer_ip,
                        "locale": "vn",
                        "order_info": order_info,
                        "expire_date": expire_date.strftime("%Y-%m-%d:%H:%M:%S")
                    }
                ),
                headers={
                    "Content-type": "application/json"
                }
            )

            resp_data = resp.json()

            if resp_data["status"] == 1:
                return resp_data["data"]["url"], True
            
            print(resp_data)
            return "", False
        except Exception as e:
            print(e)
            return "", False
        
    def calculate_bill(self, booking_id: str, promotion: Promotion = None) -> Union[int, CalculateBillErrorEnum]:
        try:
            bill_value = 0

            for seat in Booking.objects.get(id=booking_id).seats.all():
                _ticket_price = seat.ticket_type.price
                bill_value = bill_value + _ticket_price

                for fee in seat.ticket_type.ticket_type_details.all():
                    if fee.fee_type == FeeTypeEnum.cash:
                        bill_value = bill_value + fee.fee_value
                    elif fee.fee_type == FeeTypeEnum.percent:
                        bill_value = bill_value + _ticket_price*fee.fee_value/100

            if promotion is not None:
                if not self.__verify_promotion(bill_value, promotion):
                    return -1, CalculateBillErrorEnum.INVALID_PROMOTION
                
                bill_value = bill_value - {
                    DiscountTypeEnum.cash: lambda v, p: p.discount_value,
                    DiscountTypeEnum.percent: (lambda v, p: p.maximum_reduction_amount 
                                               if v*p.discount_value/100 > p.maximum_reduction_amount 
                                               else v*p.discount_value/100
                                            )
                }[promotion.discount_type](bill_value, promotion)

            return bill_value, CalculateBillErrorEnum.OK
        except Exception as e:
            print(e)
            raise e
        
    def __verify_promotion(self, total_bill: int, promotion: Promotion) -> bool:
        ok = {
            PromotionEvaluationConditionEnum.gt: lambda x: x > promotion.evaluation_value,
            PromotionEvaluationConditionEnum.gte: lambda x: x >= promotion.evaluation_value,
            PromotionEvaluationConditionEnum.lt: lambda x: x < promotion.evaluation_value,
            PromotionEvaluationConditionEnum.lte: lambda x: x <= promotion.evaluation_value,
        }[promotion.condition](total_bill)

        return ok

    def update_booking(self, payment_id: int, booking_id: str, paid_at: datetime.datetime) -> bool:
        try:
            booking = Booking.objects.get(id=booking_id)
            tickets = []

            for seat in booking.seats.all():
                tickets.append(
                    UserTicket(
                        user_id=booking.user_id,
                        seat=seat,
                        is_refunded=False,
                        payment_id=payment_id,
                        paid_at=paid_at
                    )
                )

            UserTicket.objects.bulk_create(tickets)
            return True
        except Exception as e:
            print(e)
            return False
            
    def verify_booking_id(self, booking_id: str) -> bool:
        return bool(cache.keys(f"booking:{booking_id}:seat:*"))

