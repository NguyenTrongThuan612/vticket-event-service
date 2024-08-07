import json
import pytz
import requests
import datetime
import dataclasses
from uuid import uuid4
from typing import Tuple, Union

from django.utils import timezone
from django.db import transaction
from django.core.cache import cache
from django.forms import ValidationError
from django.db.models import Q, Case, When, Value, BooleanField

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
from vticket_app.tasks.queue_tasks import async_send_email

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
        
    def calculate_bill(self, booking_id: str, promotion: Promotion = None) -> Union[int, dict, CalculateBillErrorEnum]:
        try:
            bill_value = 0
            _origin = 0
            tax = []
            _discount = 0

            for seat in Booking.objects.get(id=booking_id).seats.all():
                _ticket_price = seat.ticket_type.price
                bill_value = bill_value + _ticket_price
                _origin = _origin + _ticket_price

                for fee in seat.ticket_type.ticket_type_details.all():
                    _tax = 0

                    if fee.fee_type == FeeTypeEnum.cash:
                        _tax = fee.fee_value
                    elif fee.fee_type == FeeTypeEnum.percent:
                        _tax = _ticket_price*fee.fee_value/100

                    tax.append(
                        {
                            "name": fee.name,
                            "value": _tax
                        }
                    )

                    bill_value = bill_value + _tax

            if promotion is not None:
                if not self.__verify_promotion(bill_value, promotion):
                    return -1, None, CalculateBillErrorEnum.INVALID_PROMOTION
                
                _discount = {
                    DiscountTypeEnum.cash: lambda v, p: p.discount_value,
                    DiscountTypeEnum.percent: (lambda v, p: p.maximum_reduction_amount 
                                               if v*p.discount_value/100 > p.maximum_reduction_amount 
                                               else v*p.discount_value/100
                                            )
                }[promotion.discount_type](bill_value, promotion)

                bill_value = bill_value - _discount

            calculate_detail = {
                "origin": _origin,
                "tax": tax,
                "discount": _discount
            }

            return bill_value, calculate_detail, CalculateBillErrorEnum.OK
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

    def get_usable_promotions_by_booking(self, event: Event, bill_value: int) -> list[Promotion]:
        try:
            _today = datetime.datetime.now().date()

            base_conditions = Q(
                event=event,
                deleted_at=None,
                start_date__lte=_today,
                end_date__gte=_today,
                quantity__gt=0
            )

            case_conditions = Q(
                Q(condition=PromotionEvaluationConditionEnum.gte.value, evaluation_value__lte=bill_value) |
                Q(condition=PromotionEvaluationConditionEnum.gt.value, evaluation_value__lt=bill_value) |
                Q(condition=PromotionEvaluationConditionEnum.lte.value, evaluation_value__gte=bill_value) |
                Q(condition=PromotionEvaluationConditionEnum.lt.value, evaluation_value__gt=bill_value)
            )

            promotions = Promotion.objects.filter(base_conditions & case_conditions)

            promotion_keys_in_cache = cache.keys("booking:*:discount:*")
            num_promotions_in_cache = {}

            for key in promotion_keys_in_cache:
                pid = int(key.split(":")[-1])

                if pid in num_promotions_in_cache:
                    num_promotions_in_cache[pid] = num_promotions_in_cache[pid] + 1
                else:
                    num_promotions_in_cache[pid] = 1

            useable_promotions = []

            for promotion in promotions:
                if promotion.id in num_promotions_in_cache:
                    if promotion.quantity - num_promotions_in_cache[promotion.id] <= 0:
                        continue
                useable_promotions.append(promotion)

            return useable_promotions
        except Exception as e:
            print(e)
            return []
        
    def get_tickets_sold_by_event_id(self, event_id: int, start_date: str, end_date: str) -> dict:
        if start_date is not None:
            try:
                start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
            except ValueError:
                raise ValidationError("start_date phải có định dạng YYYY-MM-DD")
        if end_date is not None:
            try:
                end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
            except ValueError:
                raise ValidationError("end_date phải có định dạng YYYY-MM-DD")
        
        if start_date > end_date:
            start_date, end_date = end_date, start_date

        today = datetime.date.today()
        if end_date > today:
            end_date = today
        
        event = Event.objects.get(id=event_id)
        if end_date > event.start_date:
            end_date = event.start_date - datetime.timedelta(days=1)
        
        if end_date - start_date > datetime.timedelta(days=9):
            start_date = end_date - datetime.timedelta(days=9)

        date_range = [start_date + datetime.timedelta(days=x) for x in range((end_date - start_date).days + 1)]

        ticket_process_data = []
        for single_date in date_range:
            tickets_sold = UserTicket.objects.filter(
                        seat__ticket_type__event_id=event_id,
                        paid_at__date=single_date,
                        is_refunded=False
                    ).count()
            
            ticket_process_data.append({
                'date': single_date,
                'tickets_sold': tickets_sold
            })

        return ticket_process_data

    def send_e_ticket(self, payment_id: str):
        try:
            tickets = UserTicket.objects.filter(payment_id=payment_id)

            resp = requests.get(url=f"{RelatedService.account}/user/{tickets[0].user_id}/internal").json()
            print("resp = ", resp)

            if resp["status"] != 1:
                return

            mail_data = {
                "payment_id": payment_id,
                "paid_at": tickets[0].paid_at,
                "email": resp["data"]["email"],
                "fullname": resp["data"]["first_name"] + " " + resp["data"]["last_name"],
                "tickets": []
            }

            for ticket in tickets:
                mail_data["tickets"].append(
                    {
                        "seat": ticket.seat.position + str(ticket.seat.seat_number),
                        "ticket_type": ticket.seat.ticket_type.name,
                        "ticket_price": ticket.seat.ticket_type.price,
                    }
                )

            async_send_email.apply_async(
                kwargs={
                    "to": [resp["data"]["email"]],
                    "cc": [],
                    "subject": f"[Vticket] Vé điện tử",
                    "template_name": "ticket.html",
                    "context": mail_data
                }
            )
        except Exception as e:
            print(e)