from django.db import models
from django.core.validators import MinValueValidator

from vticket_app.enums.fee_type_enum import FeeTypeEnum
from vticket_app.models.ticket_type import TicketType

class TicketTypeDetail(models.Model):
    class Meta:
        db_table = "ticket_type_detail"

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=500)
    fee_type = models.CharField(choices=FeeTypeEnum.choices, default=FeeTypeEnum.cash)
    fee_value = models.IntegerField(validators=[MinValueValidator(0)])
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE, related_name="ticket_type_details")